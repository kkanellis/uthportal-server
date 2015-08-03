#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce311(CourseTask):
    document_prototype = {
        "code": "ce311",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX295"
        },
        "info": {
            "name": u"Εισαγωγή στη Θεωρία Υπολογισμού",
            "code_site": u"HY311",
            "code_eclass": u"MHX295",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX295/"
        }
    }

