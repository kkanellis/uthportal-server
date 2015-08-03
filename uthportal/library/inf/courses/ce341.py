#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce445(CourseTask):
    document_prototype = {
        "code": "ce341",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX264"
        },
        "info": {
            "name": u"Τηλεπικοινωνιακά Συστήματα",
            "code_site": u"HY341",
            "code_eclass": u"MHX264",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX264/"
        }
    }

