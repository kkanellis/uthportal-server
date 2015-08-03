#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce215(CourseTask):
    document_prototype = {
        'code': 'ce215',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX118'
        },
        'info': {
            'name': u'Αλγόριθμοι',
            'code_site': u'HY215',
            'code_eclass': u'MHX118',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX118/'
        }
    }

