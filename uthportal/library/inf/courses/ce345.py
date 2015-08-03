#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce345(CourseTask):
    document_prototype = {
        'code': 'ce345',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX267'
        },
        'info': {
            'name': u'Αναγνώριση Προτύπων',
            'code_site': u'HY345',
            'code_eclass': u'MHX267',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX267/'
        }
    }

