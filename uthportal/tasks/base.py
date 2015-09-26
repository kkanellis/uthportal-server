
import sys
from abc import ABCMeta, abstractmethod
from datetime import datetime

import feedparser
import requests
from requests.exceptions import ConnectionError, Timeout

from uthportal.database.mongo import MongoDatabaseManager
from uthportal.logger import get_logger
from uthportal.util import truncate_str

class BaseTask(object):
    __metaclass__ = ABCMeta

    def __init__(self, path, settings, database_manager, **kwargs):
        self.settings = settings
        self.path = path
        self.id = path.split('.')[-1]

        self.logger = get_logger(self.id, self.settings)

        self.timeout = self.settings['network']['timeout']
        self.database_manager = database_manager

        self.db_collection = '.'.join( path.split('.')[:-1] )

        self.db_query = { }
        for (key, value) in self.db_query_format.iteritems():
            if not hasattr(self, value):
                self.logger.error('Missing "%s" field defined in db_query_format' % value)
                sys.exit(1)

            self.db_query[key] = getattr(self, value)

        # Load and update database document (if necessary)
        self.document = self.load()
        if not self.document:
            if hasattr(self, 'document_prototype'):
                self.logger.info('No document found in database. Using prototype')
                self.document = self.document_prototype
                self.save()
            else:
                self.logger.error('No document_prototype is available!')
                return

    def __call__(self):
        """This is the method called from the Scheduler when this object is
        next in queue (and about to be executed) """

        if not hasattr(self, 'document') or not self.document:
            self.logger.error('Task has no document attribute or document is empty. Task stalled!')
        else:
            self.load()
            self.update()


    def fetch(self, link, session=None, *args, **kwargs):
        """
        Fetch a remote document to be parsed later.
        This function is called as is from subclasses
        """

        if not session:
            session = requests.Session()

        self.logger.debug('Fetching "%s" ...' % link)
        try:
            page = session.get(link, *args, timeout=self.timeout, **kwargs)
        except ConnectionError:
            self.logger.warning('%s: Connection error' % link)
            return None
        except Timeout:
            self.logger.warning('%s: Timeout [%d]' % (link, self.timeout))
            return None

        if page.status_code is not (200 or 301):
            self.logger.warning('%s: Returned [%d]' % (link, page.status_code))
            return None

        self.logger.debug('Fetched successfully! [%d]' % page.status_code)

        # Change page encoding to utf-8 so no special handling for encoding is needed
        page.encoding = 'utf-8'

        return page.text

    @abstractmethod
    def update(self, *args, **kwargs):
        """This function is called from __call__. Takes as a key-word argument (kwargs) a dictionary called
            new_fields where new data are stored after fecthing procedures. These are compared with the
            current data (stored in self.document)"""

        # Check if 'new_fields' arg is present
        if 'new_fields' in kwargs:
            new_fields = kwargs['new_fields']
        else:
            self.logger.warning('Update method called without "new_fields" dict')
            return

        # Check if 'new_fields' has the neccessary fields
        for field in self.update_fields:
            if field not in new_fields:
                self.logger.error('Field "%s" not present in "new_fields" dict. Stalling task!' % field)
                return

        # Get self.document's update_fields
        old_fields = { field: self._get_document_field(self.document, field)
                            for field in self.update_fields }

        # Check if new data is available
        (data_differ, should_notify) = self.process_new_data(new_fields, old_fields)

        now = datetime.now()
        if data_differ:
            self.logger.debug('Archiving old document...')
            self.archive()

            # Update new fields
            self.logger.debug('Updating new fields...')
            for field in self.update_fields:
                self._set_document_field(self.document, field, new_fields[field])

            # Update remaining fields
            self._set_document_field(self.document, 'first_updated', now)
            self._set_document_field(self.document, 'last_updated', now)

            self.logger.debug('Transmitting new document...')
            self.transmit()

            if should_notify:
                self.logger.debug('Notifing clients...')
                self.notify()
        else:
            self.logger.debug('No new entries found')
            self._set_document_field(self.document, 'last_updated', now)

        self.save()
        self.logger.debug('Task updated successfully!')

        self.post_process()

    def process_new_data(self, new_fields, old_fields):
        """
        Returns tuple (data_differ[bool], should_notify[bool])

        data_differ:   True if we have differences between new and old data
        should_notify: True if we have to send push notification to the client
        """

        data_differ = should_notify = False

        # Checking for differences in the according update_fields
        for field in self.update_fields:
            (old_data, new_data) = (old_fields[field], new_fields[field])

            if old_data:
                if new_data:
                    if type(old_data) == type(new_data):

                        # TODO: Better difference detection based on data type (list, dict, etc)
                        differ = True if old_data != new_data else False
                        notify = differ
                    else:
                        self.logger.warning(
                            'Different type (%s - %s) for the same field [%s]'
                                % (type(old_data), type(new_data), field)
                        )
                        differ = notify = True
                else:
                    # We shouldn't notify the user because it may be server error:
                    # e.g problematic parser or invalid link
                    differ = True
                    notify = False
            else:
                # Data differ only if new_data exist
                differ = True if new_data else False

                # We notify the user only if the task is not run for the 1st time
                notify = True if 'first_updated' in self.document else False

            if differ:
                self.logger.info(
                    truncate_str( 'New entries in field "%s"' % field, 150 )
                )

            data_differ = data_differ or differ
            should_notify = should_notify or notify

        return (data_differ, should_notify)

    def notify(self):
        pass

    def post_process(self):
        pass

    """ Database related method """

    def save(self, *args, **kwargs):
        """Save result dictionary in database"""
        if not self.database_manager.update_document(
                self.db_collection,
                self.db_query,
                self.document.copy(),
                upsert=True,
                *args,
                **kwargs):
            self.logger.warning('Could not save document "%s"' % self.path)

    def archive(self, *args, **kwargs):
        """ Save the current document into the history collection """
        if not self.database_manager.insert_document(
                'history.%s' % self.db_collection,
                self.document.copy(),
                *args,
                **kwargs):
            self.logger.warning('Could not archive document "%s"' % self.path)

    def transmit(self, *args, **kwargs):
        """ Save the current document into the server collection free of uneccessary fields """
        #TODO: Implement ignore_fields

        if not self.database_manager.update_document(
                'server.%s' % self.db_collection,
                self.db_query,
                self.document,
                *args, upsert=True, **kwargs):
            self.logger.warning('Could not transmit document "%s"' %self.path)
        pass

    def load(self, *args, **kwargs):
        """Load old dictionary from database"""
        document = self.database_manager.find_document(
                self.db_collection,
                self.db_query,
                *args,
                **kwargs)

        if document and '_id' in document:
            del document['_id']

        return document

    """ Helper methods """

    def _set_document_field(self, document, field, value):
        """ Sets the field (dot notation format) in the provided document """
        keys = field.split('.')
        for key in keys[:-1]:
            if key not in document:
                self.logger.warning('Key "%s" not found in field "%s"' % (key, field))
                return

            document = document[key]

        # Set the field
        document[keys[-1]] = value

    def _get_document_field(self, document, field):
        """ Gets the field (dot notation format) in the provided document """
        keys = field.split('.')
        for key in keys[:-1]:
            if key not in document:
                self.logger.warning('Key "%s" not found in field "%s"' % (key, field))
                return

            document = document[key]

        if keys[-1] in document:
            return document[keys[-1]]
        else:
            return None

