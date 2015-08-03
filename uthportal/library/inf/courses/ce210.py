#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce210(CourseTask):
    document_prototype = {
        'code': 'ce210',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX257'
        },
        'info': {
            'name': u'Δομές Δεδομένων',
            'code_site': u'HY210',
            'code_eclass': u'MHX257',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX257/'
        }
    }

