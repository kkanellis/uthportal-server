#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce530(CourseTask):
    document_prototype = {
        'code': 'ce530',
        'code_eclass': u'MHX248',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX248'
        },
        'info': {
            'name': u'Προσομοίωση Κυκλωμάτων',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX248/'
        }
    }

