#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ee151(CourseTask):
    document_prototype = {
        'code': 'ee151',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX322'
        },
        'info': {
            'name': u'Εισαγωγή στο Σχέδιο και τα Ηλεκτροτεχνικά Υλικά',
            'code_site': u'HM151',
            'code_eclass': u'MHX322',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX322/'
        }
    }

