#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ee340(CourseTask):
    document_prototype = {
        "code": "ee340",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX288"
        },
        "info": {
            "name": u"Συστήματα Αυτομάτου Ελέγχου",
            "code_site": u"HM340",
            "code_eclass": u"MHX288",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX288/"
        }
    }

