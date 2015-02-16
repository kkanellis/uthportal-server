import logging
from abc import ABCMeta, abstractmethod
from datetime import datetime

import feedparser
import requests
from requests.exceptions import ConnectionError, Timeout

from uthportal.database.mongo import MongoDatabaseManager
from uthportal.logger import get_logger, logging_level

class BaseTask(object):
    __metaclass__ = ABCMeta

    def __init__(self, path, timeout, database_manager, **kwargs):
        self.logger = get_logger('%s.%s' % (__name__, self.__class__.__name__), logging_level.DEBUG)

        self.path = path
        self.timeout = timeout
        self.database_manager = database_manager

        self.id = path.split('.')[-1]
        self.db_collection = ''.join( path.split('.')[:-1] )

    def __call__(self):
        """This is the method called from the Scheduler when this object is
        next in queue"""
        print self.document
        self.update()

    def fetch(self, link):
        """Fetch a remote document to be parsed later"""
        try:
            page = requests.get(link, timeout=self.timeout)
        except ConnectionError:
            self.logger.warning('%s: Connection error' % link)
            return None
        except Timeout:
            self.logger.warning('%s: Timeout [%d]' % (link, self.timeout))
            return None

        if page.code is not (200 or 301):
            self.logger.warning('%s: Returned [%d]' % (link, page.code))
            return None

        page.encoding = 'utf-8'
        return page.text

    @abstractmethod
    def update(self, *args, **kwargs):
        """This function is called from __call__. Takes as a key-word argument (kwargs) a dictionary called
            new_fields where new data are stored after fecthing procedures. These are compared with the
            current data (stored in self.document)"""

        #Check if 'new_fields' arg is present
        if 'new_fields' in kwargs:
            new_fields = kwargs['new_fields']
        else:
            self.logger.warning('Update method called without "new_fields" dict')
            return

        #Check if 'new_fields' has the neccessary fields
        for field in self.update_fields:
            if field not in new_fields:
                self.logger.warning('Field "%s" not present in "new_fields" dict' % field)
                return

        #Get self.document's update_fields
        old_fields = { field: self.__get_document_field(self.document, field)
                            for field in self.update_fields }

        #Checking for differences in the according update_fields """
        differ = False
        for field in self.update_fields:
            if old_fields[field] != new_fields[field]:
                self.logger.info('New entries in field "%s"' % new_fields[field])
                differ = True
                break

        now = datetime.now()
        if differ:
            self.archive()

            #Update new fields """
            for field in self.update_fields:
                self.__set_document_field(self.document, field, new_fields[field])

            #Update remaining fields """
            self.__set_document_field(self.document, 'first_updated', now)
            self.__set_document_field(self.document, 'last_updated', now)

            self.transmit()
            self.notify()
        else:
            self.__set_document_field(self.document, 'last_updated', now)

        self.save()

    def notify(self):
        pass

    """ Database related method """

    def save(self, *args, **kwargs):
        """Save result dictionary in database"""
        if not self.database_manager.update_document(self.db_collection, self.db_query, self.document, *args, **kwargs):
            self.logger.warning('Could not save document "%s"' % self.path)

    def archive(self, *args, **kwargs):
        """ Save the current document into the history collection """
        if not self.database_manager.insert_document('history.%s' % self.db_collection, self.document, *args, **kwargs):
            self.logger.warning('Could not archive document "%s"' % self.path)

    def transmit(self, *args, **kwargs):
        """ Save the current document into the server collection free of uneccessary fields """
        #TODO: Implement ignore_fields

        if not self.database_manager.update_document('server.%s' % self.db_collection, self.document, *args, **kwargs):
            self.logger.warning('Could not transmit document "%s"' %self.path)
        pass

    def load(self, *args, **kwargs):
        """Load old dictionary from database"""
        return self.database_manager.find_document(self.db_collection, self.db_query, *args, **kwargs)

    """ Helper methods """

    def __set_document_field(self, document, field, value):
        """ Sets the field (dot notation format) in the provided document """
        keys = field.split('.')
        for key in keys[:-1]:
            if key not in document:
                self.logger.warning('Key "%s" not found in field "%s"' % (key, field))
                return

            document = document[key]

        # Set the field
        document[keys[-1]] = value

    def __get_document_field(self, document, field):
        """ Gets the field (dot notation format) in the provided document """
        keys = fields.split('.')
        for key in keys[:-1]:
            if key not in document:
                self.logger.warning('Key "%s" not found in field "%s"' % (key, field))
                return

            document = document[key]

        if key[-1] in document:
            return document[key]
        else:
            return None

"""
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    a = CourseTask('inf.courses.ce120', 5, MongoDatabaseManager())
"""
