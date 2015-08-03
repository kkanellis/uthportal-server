#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce331(CourseTask):
    document_prototype = {
        'code': 'ce331',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX269'
        },
        'info': {
            'name': u'Ηλεκτρομαγνητικά Πεδία I',
            'code_site': u'HY331',
            'code_eclass': u'MHX269',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX269/'
        }
    }

