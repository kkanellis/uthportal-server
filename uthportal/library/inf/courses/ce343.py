#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce343(CourseTask):
    document_prototype = {
        "code": "ce343",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX185"
        },
        "info": {
            "name": u"Ψηφιακή Επεξεργασία Εικόνας",
            "code_site": u"HY343",
            "code_eclass": u"MHX185",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX185/"
        }
    }

