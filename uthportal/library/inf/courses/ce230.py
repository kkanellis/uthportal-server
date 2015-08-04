#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

from uthportal.library.inf.courses.ce232 import parse as parse_ce232

class ce230(CourseTask):
    document_prototype = {
        'code': 'ce230',
        'announcements': {
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE230/',
            'link_eclass': '',
        },
        'info': {
            'name': u'Ανάλυση Κυκλωμάτων',
            'code_site': 'HY230',
            'code_eclass': '',
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE230/',
            'link_eclass': ''
        }
    }

    def parse_site(self, bsoup):
        return parse_ce232(bsoup)

