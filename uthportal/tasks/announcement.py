
import pkgutil
from abc import ABCMeta, abstractmethod

import requests

from uthportal.tasks.base import BaseTask
from uthportal.util import get_soup

class AnnouncementTask(BaseTask):
    task_type = 'AnnouncementTask'

    def __init__(self, path, settings, database_manager, **kwargs):
        super(AnnouncementTask, self).__init__(path, settings, database_manager)

        self.update_fields = ['entries']
        self.db_query = { 'type': self.id }

        self.logger.debug('Loading document from database...')

        self.document = self.load()
        if not self.document:
            if hasattr(self, 'document_prototype'):
                self.logger.info('No document found in database. Using prototype')
                self.document = self.document_prototype
                self.save()
            else:
                self.logger.error('No document_prototype is available!')
                return

        self.logger.debug('id = {:<10} | collection = {:<35}'.format(self.id, self.db_collection))


    def parse(self, bsoup):
        """Parse the fetced document"""
        return None

    def update(self):
        new_document_fields = {
            'entries': self._check_source()
        }

        # Check any new data exist
        if any( field_data for field_data in new_document_fields.items() ):
            super(AnnouncementTask, self).update(new_fields=new_document_fields)
        else:
            self.logger.warning('No dictionary field contains new data.')

    def _check_source(self):
        link = self.document['link']
        (session, auth_success) = self._check_auth()

        if not auth_success:
            self.logger.error('Authentication failed..')
            return None

        html = self.fetch(link, session=session)
        if not html:
            self.logger.warning('Fetch "%s" returned nothing' % link)
            return None

        bsoup = get_soup(html)
        if not bsoup:
            self.logger.warning('BeautifulSoup returned None')
            return None

        try:
            entries = self.parse(bsoup)
        except Exception, e:
            self.logger.error('parse: %s' % unicode(e))
            return None

        return entries

    def _check_auth(self):
        session = None
        auth_id = self._get_document_field(self.document, 'auth_type')

        if auth_id:
            self.logger.debug('Authentication is needed. Initiating proccess...')

            # Retrieve document which contains info on how to auth
            auth_info = self._get_auth_info(auth_id)
            if (not auth_info or
                not set(['link', 'payload', 'method']) <= set(auth_info)):
                    self.logger.error('Not a valid auth_info dict for "%s"' % unicode(auth_id))
                    return (None, False)

            (link, payload, method_str) = (auth_info['link'], auth_info['payload'], auth_info['method'])

            # Load & execute module
            module = pkgutil.find_loader('uthportal.tasks.auth_methods').load_module('')
            auth_method = getattr(module, method_str)

            session = requests.Session()
            response = auth_method(session, link, payload)

            if not response:
                self.logger.error('Could not be auth @ "%s"' % link)
                return (None, False)

            self.logger.debug('Auth: success')
            return (session, response)
        else:
            return (session, True)


    # NOTE: Ignore atm
    def _get_auth_info(self, type):
        query = { 'type' : type }
        document = self.database_manager.find_document('auth_info', query)

        if document and '_id' in document:
            del document['_id']
            return document
        else:
            self.logger.error('No auth info found for type "%s"' % type)
