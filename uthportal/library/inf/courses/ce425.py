#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce425(CourseTask):
    document_prototype = {
        "code": "ce425",
        "announcements": {
            "link_site": "http://inf-server.inf.uth.gr/mavcourses/wis/feed/",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX274"
        },
        "info": {
            "name": u"Πληροφορικά Συστήματα στον Παγκόσμιο Ιστό",
            "code_site": u"HY425",
            "code_eclass": u"MHX274",
            "link_site": "http://inf-server.inf.uth.gr/mavcourses/wis/",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX274/"
        }
    }
