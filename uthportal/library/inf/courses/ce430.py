#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce430(CourseTask):
    document_prototype = {
        "code": "ce430",
        "code_eclass": u"MHX286",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX286"
        },
        "info": {
            "name": u"Εργαστήριο Ψηφιακών Κυκλωμάτων",
            "link_site": "http://inf-server.inf.uth.gr/courses/CE430/",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX286/"
        }
    }

