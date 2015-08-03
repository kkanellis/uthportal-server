#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask
from uthportal.util import parse_rss

class ce211(CourseTask):
    document_prototype = {
        'code': 'ce211',
        'announcements': {
            'link_site': 'http://inf-server.inf.uth.gr/mavcourses/diaeks/feed/',
            'link_eclass': ''
        },
        'info': {
            'name': u'Διαφορικές Εξισώσεις',
            'code_site': 'HY211',
            'code_eclass': '',
            'link_site': 'http://inf-server.inf.uth.gr/mavcourses/diaeks/',
            'link_eclass': ''
        }
    }

    def parse_site(self, bsoup):
        return parse_rss( unicode(bsoup) )

