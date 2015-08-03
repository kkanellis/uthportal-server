#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce327(CourseTask):
    document_prototype = {
        "code": "ce327",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX112"
        },
        "info": {
            "name": u"Ανάκληση Πληροφορίας",
            "code_site": u"HY327",
            "code_eclass": u"MHX112",
            "link_site": "http://inf-server.inf.uth.gr/courses/CE327/",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX112/"
        }
    }

