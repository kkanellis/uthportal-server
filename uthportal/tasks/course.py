from datetime import datetime
from abc import ABCMeta, abstractmethod

import feedparser
from bs4 import BeautifulSoup

from uthportal.tasks.base import BaseTask
from uthportal.util import fix_urls, get_soup, parse_rss

class CourseTask(BaseTask):
    task_type = 'CourseTask'

    update_fields = ['announcements.site', 'announcements.eclass']
    notify_fields = ['info.name', 'info.code_site']
    db_query_format = { 'code' : 'id' }

    def __init__(self, path, settings, database_manager, pushd_client):
        super(CourseTask, self).__init__(path, settings, database_manager, pushd_client)

        # Calculate semester of course based on course code
        year, _, spring = self.id[2:]
        semester = (2 * int(year)) if int(spring) % 2 == 1 else (2 * int(year) - 1)
        self._set_document_field(self.document, 'info.semester', semester)
        self.save()

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
            entries = self.fix_site_entries(entries, link)
        except Exception as e:
            self.logger.error('fix_site_entries: %s', unicode(e))
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

        try:
            entries = self.fix_eclass_entries(entries)
        except Exception as e:
            self.logger.error('fix_eclass_entries: %s', unicode(e))
            return None

        return entries

    def parse_site(self, bsoup):
        """Parse the fetced document"""
        return None

    def fix_site_entries(self, entries, base_link):
        """ Process the document before saving
            For each entry:
                a) convert all relative links to absolute ones
                b) add a title if no title is present
        """

        for entry in entries:
            entry['html'] = fix_urls(entry['html'], base_link)

            if 'title' not in entry or not entry['title']:
                entry_date_str = entry['date'].strftime('%2d/%2m/%4Y')
                code_site = self._get_document_field(self.document, 'info.code_site')
                entry['title'] = '%s - %s' % (code_site, entry_date_str)

            if 'link' not in entry:
                entry['link'] = self._get_document_field(self.document, 'announcements.link_site')

        return entries

    def fix_eclass_entries(self, entries):
        """ Process the document before saving
            For each entry:
                a) add a title if no title is present
        """

        for entry in entries:
            if 'title' not in entry or not entry['title']:
                entry_date_str = entry['date'].strftime('%2d/%2m/%4Y')
                code_eclass = self._get_document_field(self.document, 'info.code_eclass')
                entry['title'] = '%s - %s' % (code_eclass, entry_date_str)

        return entries

