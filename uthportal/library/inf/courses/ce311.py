#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce311(CourseTask):
    document_prototype = {
        'code': 'ce311',
        'code_eclass': u'MHX275',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX275'
        },
        'info': {
            'name': u'Θεωρία Υπολογισμού',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX275/'
        }
    }

