#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce330(CourseTask):
    document_prototype = {
        'code': 'ce330',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX290'
        },
        'info': {
            'name': u'Ψηφιακά Ηλεκτρονικά',
            'code_site': u'HY330',
            'code_eclass': u'MHX290',
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE330/',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX290/'
        }
    }

