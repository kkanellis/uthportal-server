#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce110(CourseTask):
    document_prototype = {
        'code': 'ce110',
        'announcements': {
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX159'
        },
        'info': {
            'name': u'Μαθηματικός Λογισμός Ι',
            'code_site': u'HY110',
            'code_eclass': u'MHX159',
            'link_site': '',
            'link_eclass': 'http://eclass.uth.gr/eclass/courses/MHX159/',
        }
    }

