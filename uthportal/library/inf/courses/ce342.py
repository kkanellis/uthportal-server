#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce342(CourseTask):
    document_prototype = {
        'code': 'ce342',
        'code_eclass': u'MHX256',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX256'
        },
        'info': {
            'name': u'Ψηφιακή Επεξεργασία Σήματος',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX256/'
        }
    }

