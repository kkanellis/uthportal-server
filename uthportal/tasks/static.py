
from abc import ABCMeta, abstractmethod

from uthportal.tasks.base import BaseTask
from uthportal.util import get_soup

class StaticTask(BaseTask):
    task_type = 'StaticTask'

    def __init__(self, path, settings, database_manager, **kwargs):
        super(StaticTask, self).__init__(path, settings, database_manager)

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

    def fetch(self):
        filepath = self.filedir + '/' + self.filename
        print filepath
        try:
            with open(filepath, 'r') as f:
                html = f.read().decode('utf8')
        except IOError as e:
            print 'Cannot read from "%s". Please make sure the file exists' % self.path
            return

        return html

    def update(self):
        new_document_fields = {
            'entries': self._check_source()
        }

        # Check any new data exist
        if any( field_data for field_data in new_document_fields.items() ):
            super(StaticTask, self).update(new_fields=new_document_fields)
        else:
            self.logger.warning('No dictionary field contains new data.')

    def _check_source(self):
        html = self.fetch()
        if not html:
            self.logger.warning('Fetch returned nothing. Make sure the file exist')
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

