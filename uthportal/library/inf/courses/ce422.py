#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce422(CourseTask):
    document_prototype = {
        "code": "ce422",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX312"
        },
        "info": {
            "name": u"Εξόρυξη Δεδομένων",
            "code_site": u"HY422",
            "code_eclass": u"MHX312",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX312/"
        }
    }

