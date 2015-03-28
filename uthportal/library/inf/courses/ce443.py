#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce443(CourseTask):
    document_prototype = {
        'code': 'ce443',
        'code_eclass': u'MHX272',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX272'
        },
        'info': {
            'name': u'Όραση Υπολογιστών',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX272/'
        }
    }

