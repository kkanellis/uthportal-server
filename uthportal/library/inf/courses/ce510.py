#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce510(CourseTask):
    document_prototype = {
        "code": "ce510",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX210"
        },
        "info": {
            "name": u"Βιοπληροφορική",
            "code_site": u"HY510",
            "code_eclass": u"MHX210",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX210/"
        }
    }

