#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce410(CourseTask):
    document_prototype = {
        "code": "ce410",
        "announcements": {
            "link_site": "http://inf-server.inf.uth.gr/courses/CE410/news.html",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX251"
        },
        "info": {
            "name": u"Παράλληλοι και Δικτυακοί Υπολογισμοί",
            "code_site": "HY410",
            "code_eclass": "MHX251",
            "link_site": "http://inf-server.inf.uth.gr/courses/CE410/",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX251/"
        }
    }

