#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ee250(CourseTask):
    document_prototype = {
        'code': 'ee250',
        'code_eclass': u'MHX293',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX293'
        },
        'info': {
            'name': u'Ηλεκτρικές Μετρήσεις',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX293/'
        }
    }

