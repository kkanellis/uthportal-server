from time import mktime
from datetime import datetime

import feedparser
from bs4 import BeautifulSoup

from uthportal.tasks.base import BaseTask
from uthportal.util import fix_urls, get_soup

class CourseTask(BaseTask):
    task_type = 'CourseTask'

    def __init__(self, path, file_path, timeout, database_manager):
        super(CourseTask, self).__init__(path, file_path, timeout, database_manager)

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

        self.logger.debug('id = {:<10} | collection = {:<35}'.format(self.id, self.db_collection))

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

        bsoup = get_soup(html)
        if not bsoup:
            self.warning('BeautifulSoup returned None')
            return None

        try:
            entries = self.parse_site(bsoup)
        except Exception, e:
            self.logger.error('parse_site: %s', unicode(e))
            return None

        try:
            entries = self.postprocess_site(entries, link)
        except Exception, e:
            self.logger.error('post_process: %s', unicode(e))
            return None

        return entries

    def __check_eclass(self):
        link = self._get_document_field(self.document, 'announcements.link_eclass')
        if not link:
            self.logger.info('"link_eclass" not found in document!')
            return None

        html = self.fetch(link)
        if not html:
            self.logger.warning('Fetch "%s" returned nothing' % link)
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
                        'plaintext': get_soup(entry.description).text,
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
        """ Process the document before saving
            For each entry:
                a) convert all relative links to absolute ones
                b) adds a title if no title is present
        """

        for entry in entries:
            entry['html'] = fix_urls(entry['html'], base_link)

            if 'title' not in entry:
                entry_date_str = entry['date'].strftime('%2d/%2m/%4Y')
                entry['title'] = '%s - %s' % (self.id.upper(), entry_date_str)

        return entries

