#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce416(CourseTask):
    document_prototype = {
        "code": "ce416",
        "announcements": {
            "link_site": "",#"http://inf-server.inf.uth.gr/courses/CE416/admin/news.html",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX101"
        },
        "info": {
            "name": "Γραφικά Η/Υ",
            "code_site": u"HY416",
            "code_eclass": "MHX101",
            "link_site": "http://inf-server.inf.uth.gr/courses/CE416/",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX101/"
        }
    }

