#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce111(CourseTask):
    document_prototype = {
        'code': 'ce111',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX172'
        },
        'info': {
            'name': u'Λογισμός ΙΙ',
            'code_site': u'HY111',
            'code_eclass': u'MHX172',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX172/'
        }
    }

