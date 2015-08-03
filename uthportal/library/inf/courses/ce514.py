#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce514(CourseTask):
    document_prototype = {
        'code': 'ce514',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX258'
        },
        'info': {
            'name': u'Περιβάλλοντα Επίλυσης Προβλημάτων',
            'code_site': u'HY514',
            'code_eclass': u'MHX258',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX258/'
        }
    }

