#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce426(CourseTask):
    document_prototype = {
        'code': 'ce426',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX278'
        },
        'info': {
            'name': u'Τεχνολογίες Παγκόσμιου Ιστού',
            'code_site': u'HY426',
            'code_eclass': u'MHX278',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX278/'
        }
    }

