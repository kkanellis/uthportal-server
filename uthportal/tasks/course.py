from datetime import datetime
from abc import ABCMeta, abstractmethod

import feedparser
from bs4 import BeautifulSoup

from uthportal.tasks.base import BaseTask
from uthportal.util import fix_urls, get_soup, parse_rss

class CourseTask(BaseTask):
    task_type = 'CourseTask'

    def __init__(self, path, settings, database_manager):
        super(CourseTask, self).__init__(path, settings, database_manager)

        self.update_fields =[ 'announcements.site', 'announcements.eclass' ]
        self.db_query = { 'code' : self.id }

        self.logger.debug('Loading document from database...')

        self.document = self.load()
        if not self.document:
            if hasattr(self, 'document_prototype'):
                self.logger.info('No document found in database. Using prototype')
                self.document = self.document_prototype

                # Calculate semester of course based on course code
                year, _, spring = self.id[2:]
                semester = (2 * int(year)) if int(spring) % 2 == 1 else (2 * int(year) - 1)
                self._set_document_field(self.document, 'info.semester', semester)

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
            self.logger.debug('"link_site" not found in document!')
            return None

        html = self.fetch(link)
        if not html:
            self.logger.warning('Fetch "%s" returned nothing' % link)
            return None

        bsoup = get_soup(html)
        if not bsoup:
            self.logger.warning('BeautifulSoup returned None')
            return None

        try:
            entries = self.parse_site(bsoup)
        except Exception as e:
            self.logger.error('parse_site: %s', unicode(e))
            return None

        try:
            entries = self.postprocess_site(entries, link)
        except Exception as e:
            self.logger.error('post_process: %s', unicode(e))
            return None

        return entries

    def __check_eclass(self):
        link = self._get_document_field(self.document, 'announcements.link_eclass')
        if not link:
            self.logger.debug('"link_eclass" not found in document!')
            return None

        html = self.fetch(link)
        if not html:
            self.logger.warning('Fetch "%s" returned nothing' % link)
            return None

        self.logger.debug('Parsing eclass ...')
        try:
            entries = parse_rss(html)
        except Exception as e:
            self.logger.error('parse_rss: %s' % unicode(e))
            return None

        return entries


    # This is commented out only for testing and shouldn't.
    #@abstractmethod
    def parse_site(self, bsoup):
        """Parse the fetced document"""
        return None

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
