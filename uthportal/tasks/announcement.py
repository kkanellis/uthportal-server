
import pkgutil
from abc import ABCMeta, abstractmethod

import requests

from uthportal.tasks.base import BaseTask
from uthportal.tasks.auth import auth_classes
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

        # Check if task needs auth
        if 'auth_type' in self.document:
            auth_type = self.document['auth_type']
            auth_settings = settings['auth']

            self.logger.debug('Task need authentication using "%s" manager' % auth_type)

            if auth_type not in auth_classes:
                self.logger.error('No auth class is registered for "%s"' % auth_type)
                return

            if auth_type not in auth_settings:
                self.logger.error('No authentication settings found for "%s"' % auth_type)
                return

            self.auth_manager = auth_classes[auth_type](
                    self.logger,
                    auth_settings[auth_type]
                    )



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
        session = requests.Session()

        if hasattr(self, 'auth_manager'):
            # Perform authentication
            self.auth_manager.auth(session)
            if not self.auth_manager.success:
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

