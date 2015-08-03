#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ee452(CourseTask):
    document_prototype = {
        "code": "ee452",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX289"
        },
        "info": {
            "name": u"Ηλεκτρικές Εγκαταστάσεις",
            "code_site": u"HM452",
            "code_eclass": u"MHX289",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX289/"
        }
    }

