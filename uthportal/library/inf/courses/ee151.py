#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ee151(CourseTask):
    document_prototype = {
        'code': 'ee151',
        'code_eclass': u'MHX276',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX276'
        },
        'info': {
            'name': u'Εισαγωγή στο Σχέδιο και τα Ηλεκτροτεχνικά Υλικά',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX276/'
        }
    }

