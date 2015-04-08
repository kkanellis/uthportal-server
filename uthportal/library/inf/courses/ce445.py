#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce445(CourseTask):
    document_prototype = {
        'code': 'ce445',
        'code_eclass': u'MHX299',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX299'
        },
        'info': {
            'name': u'Ασύρματες Επικοινωνίες',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX299/'
        }
    }
