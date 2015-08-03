#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce442(CourseTask):
    document_prototype = {
        "code": "ce442",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX260"
        },
        "info": {
            "name": u"Εφαρμοσμένες Στοχαστικές Διεργασίες",
            "code_site": u"HY442",
            "code_eclass": u"MHX260",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX260/"
        }
    }

