#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce333(CourseTask):
    document_prototype = {
        'code': 'ce333',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX219'
        },
        'info': {
            'name': u'Σχεδίαση Συστημάτων VLSI',
            'code_site': u'HY333',
            'code_eclass': u'MHX219',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX219/'
        }
    }

