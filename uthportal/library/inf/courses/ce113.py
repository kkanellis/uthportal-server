#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce113(CourseTask):
    document_prototype = {
        'code': 'ce113',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX265'
        },
        'info': {
            'name': u'Διακριτά Μαθηματικά',
            'code_site': u'HY113',
            'code_eclass': u'MHX265',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX265/'
        }
    }

