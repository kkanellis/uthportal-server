#/usr/bin/env python
# -*- coding: utf-8 -*-


from uthportal.tasks.announcement import AnnouncementTask
from uthportal.util import parse_greek_date, get_soup

from uthportal.library.inf.announce.general import general

class academic(AnnouncementTask):

    document_prototype = {
        'type': 'academic',
        'link': 'http://www.inf.uth.gr/cced/?cat=50',
        'auth_type': 'inf-site'
    }

    def parse(self, bsoup):
        return general.parse(bsoup)

