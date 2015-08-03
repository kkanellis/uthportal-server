#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ee540(CourseTask):
    document_prototype = {
        "code": "ee540",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX304"
        },
        "info": {
            "name": u"Προσαρμοστικά Συστήματα Αυτόματου Ελέγχου",
            "code_site": u"HY540",
            "code_eclass": u"MHX304",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX304/"
        }
    }

