#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce150(CourseTask):
    document_prototype = {
        'code': 'ce150',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX211'
        },
        'info': {
            'name': u'Φυσική Ι',
            'code_site': u'HY150',
            'code_eclass': u'MHX211',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX211/'
        }
    }

