#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask
from uthportal.util import parse_rss

class ce112(CourseTask):
    document_prototype = {
        'code': 'ce112',
        'announcements': {
            'link_site': 'http://inf-server.inf.uth.gr/mavcourses/ga/feed/',
            'link_eclass': ''
        },
        'info': {
            'name': u'Γραμμική Άλγεβρα',
            'code_site': u'HY112',
            'code_eclass': '',
            'link_site': 'http://inf-server.inf.uth.gr/mavcourses/ga/',
            'link_eclass': '',
        }
    }

    def parse_site(self, bsoup):
        return parse_rss( unicode(bsoup) )

