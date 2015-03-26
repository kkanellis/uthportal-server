from abc import ABCMeta, abstractmethod

from uthportal.tasks.base import BaseTask
from uthportal.util import get_soup

class AnnouncementTask(BaseTask):
    task_type = 'AnnouncementTask'

    def __init__(self, path, file_path, timeout, database_manager, **kwargs):
        super(AnnouncementTask, self).__init__(path, file_path, timeout, database_manager)

        self.update_fields =['announcements']
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

        #TODO: Maybe add this in settings?(Probably not)
        link = 'http://www.inf.uth.gr/cced/?cat=24'

        html = self.fetch(link)
        if not html:
            self.warning('Fetch "%s" returned nothing' % link)
            return None

        bsoup = get_soup(html)
        if not bsoup:
            self.warning('BeautifulSoup returned None')
            return None

        new_document_fields = {
                'announcements': self.parse(bsoup)
        }

        # Check any new data exist
        if any( field_data for field_data in new_document_fields.items() ):
            super(AnnouncementTask, self).update(new_fields=new_document_fields)
        else:
            return


