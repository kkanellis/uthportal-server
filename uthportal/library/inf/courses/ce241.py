#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce241(CourseTask):
    document_prototype = {
        'code': 'ce241',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX231'
        },
        'info': {
            'name': u'Σήματα και Συστήματα',
            'code_site': u'HY241',
            'code_eclass': u'MHX231',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX231/'
        }
    }

