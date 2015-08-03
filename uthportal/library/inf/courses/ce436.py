#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce436(CourseTask):
    document_prototype = {
        'code': 'ce436',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX228'
        },
        'info': {
            'name': u'Έλεγχος και Επαλήθευση Ψηφιακών Κυκλωμάτων',
            'code_site': u'HY436',
            'code_eclass': u'MHX228',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX228/'
        }
    }

