#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ee353(CourseTask):
    document_prototype = {
        "code": "ee353",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX321"
        },
        "info": {
            "name": u"Ηλεκτρικές Μηχανές",
            "code_site": u"HM353",
            "code_eclass": u"MHX321",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX321/"
        }
    }

