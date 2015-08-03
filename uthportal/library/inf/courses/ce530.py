#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce530(CourseTask):
    document_prototype = {
        "code": "ce530",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX248"
        },
        "info": {
            "name": u"Αλγόριθμοι Προσομοίωσης Κυκλωμάτων",
            "code_site": u"HY530",
            "code_eclass": u"MHX248",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX248/"
        }
    }
