#/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.announcement import AnnouncementTask
from uthportal.util import parse_greek_date, get_soup

from uthportal.library.inf.announce.general import general

class scholarships(AnnouncementTask):

    document_prototype = {
        'name': u'Υποτροφίες',
        'type': 'scholarships',
        'link': 'http://www.inf.uth.gr/cced/?cat=12',
        'auth_type': 'inf-site'
    }

    def parse(self, bsoup):
        return general.parse(bsoup)

