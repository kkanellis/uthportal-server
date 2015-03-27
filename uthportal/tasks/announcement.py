
from abc import ABCMeta, abstractmethod

import requests

from uthportal.tasks.base import BaseTask
from uthportal.util import get_soup

class AnnouncementTask(BaseTask):
    task_type = 'AnnouncementTask'

    def __init__(self, path, file_path, settings, database_manager, **kwargs):
        super(AnnouncementTask, self).__init__(path, file_path, settings, database_manager)

        self.update_fields = ['entries']
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


    @abstractmethod
    def parse(self, document):
        """Parse the fetced document"""
        return None

    def update(self):
        """
        Fetches the announcements site, parse it
        and call base update with the new fields
        """

        link = self.document['link']

        html = self.fetch(link)
        if not html:
            self.logger.warning('Fetch "%s" returned nothing' % link)
            return None

        bsoup = get_soup(html)
        if not bsoup:
            self.logger.warning('BeautifulSoup returned None')
            return None

        new_document_fields = {
            'entries': self.parse(bsoup)
        }

        # Check any new data exist
        if any( field_data for field_data in new_document_fields.items() ):
            super(AnnouncementTask, self).update(new_fields=new_document_fields)
        else:
            self.logger.warning('No dictionary field contains new data.')

    # NOTE: Ignore atm
    def _make_auth(self, link, payload, session):
        """ Makes an http POST request in order to login where needed """
        try:
            auth_response = session.post(link, verify=False, data=payload)
        except ConnectionError:
            self.logger.warning('%s: Connection error' % link)
            return None
        except Timeout:
            self.logger.warning('%s: Timeout [%d]' % (link, self.timeout))
            return None

        if page.status_code is not (200 or 301):
            self.logger.warning('%s: Returned [%d]' % (link, page.code))
            return None

        return auth_response

    # NOTE: Ignore atm
    def _get_auth_info(self, type):
        query = { 'type' : type }
        document = self.database_manager.find_document('auth', query)

        if document and '_id' in document:
            del document['_id']
        else:
            self.logger.error('No auth info found for type "%s"' % type)

