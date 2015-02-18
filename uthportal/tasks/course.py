
import feedparser
from bs4 import BeautifulSoup

from uthportal.tasks.base import BaseTask
from uthportal.util import fix_urls

class CourseTask(BaseTask):
    task_type = 'CourseTask'

    def __init__(self, path, timeout, database_manager):
        super(CourseTask, self).__init__(path, timeout, database_manager)

        self.update_fields =[ 'announcements.site', 'announcements.eclass' ]
        self.db_query = { 'code' : self.id }

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

    def update(self):
        new_document_fields = {
                'announcements.site': self.__check_site(),
                'announcements.eclass': self.__check_eclass()
        }

        # Check any new data exist
        if any( field_data for field_data in new_document_fields.items() ):
            super(CourseTask, self).update(new_fields=new_document_fields)
        else:
            self.logger.warning('No dictionary field contains new data.')

    def __check_site(self):
        link = self._get_document_field(self.document, 'announcements.link_site')
        if not link:
            self.logger.info('"link_site" not found in document!')
            return None

        html = self.fetch(link)
        if not html:
            self.warning('Fetch "%s" returned nothing' % link)
            return None

        bsoup = self.__getsoup(html)
        if not bsoup:
            self.warning('BeautifulSoup returned None')
            return None

        try:
            entries = self.parse_site(bsoup)
        except Exception, e:
            self.logger.error(e)
            return None

        try:
            entries = self.postprocess_site(entries, link)
        except Exception, e:
            self.logger.error(e)
            return None

        return entries

    def __check_eclass(self):
        link = self._get_document_field(self.document, 'announcements.link_eclass')
        if not link:
            self.logger.info('"link_eclass" not found in document!')
            return None

        html = self.fetch(link)
        if not html:
            self.warning('Fetch "%s" returned nothing' % link)
            return None

        return self.parse_eclass(html)

    def parse_site(self, bsoup):
        """Parse the fetced document"""
        return None

    def parse_eclass(self, html):
        """Parse the fetced document"""

        self.logger.debug('Parsing eclass ...')
        try:
            rss = feedparser.parse(html)
        except Exception, e:
            self.logger.error(e)
            return None

        # Datetime format
        # dt_format = '%a, %d %b %Y %H:%M:%S %z'
        entries = None
        try:
            entries = [{
                        'title': entry.title,
                        'html': entry.description,
                        'plaintext': __get_soup(entry.description).text,
                        'link': entry.link,
                        'date': datetime.fromtimestamp(mktime(entry.published_parsed)),
                        'has_time': True
                        }
                        for entry in rss.entries ]
        except Exception, e:
            self.logger.error(e)
            return None

        self.logger.debug('Parsed eclass successfully!')
        return entries

    def postprocess_site(self, entries, base_link):
        """Process the document before saving"""

        for entry in entries:
            entry['html'] = fix_urls(entry['html'], base_link)

        return entries

    def __getsoup(self, html):
        """ Returns the BeautifulSoup object from the html """
        bsoup = None
        try:
            bsoup = BeautifulSoup(html)
        except Exception, e:
            self.logger.error('Error while parsing html: %s' % e)

        return bsoup

