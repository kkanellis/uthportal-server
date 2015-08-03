#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce231(CourseTask):
    document_prototype = {
        'code': 'ce231',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX300'
        },
        'info': {
            'name': u'Εισαγωγή στην Ηλεκτρονική',
            'code_site': u'HY231',
            'code_eclass': u'MHX300',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX300/'
        }
    }

