
import pkgutil
from abc import ABCMeta, abstractmethod

import requests

from uthportal.tasks.base import BaseTask
from uthportal.tasks.auth import auth_classes
from uthportal.util import get_soup

class AnnouncementTask(BaseTask):
    task_type = 'AnnouncementTask'

    update_fields = ['entries']
    db_query_format = { 'type': 'id' }

    def __init__(self, path, settings, database_manager, **kwargs):
        super(AnnouncementTask, self).__init__(path, settings, database_manager)

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
        except Exception as e:
            self.logger.error('parse: %s' % unicode(e))
            return None

        return entries

