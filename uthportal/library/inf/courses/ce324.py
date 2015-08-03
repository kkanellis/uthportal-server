#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce324(CourseTask):
    document_prototype = {
        "code": "ce324",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX311"
        },
        "info": {
            "name": "Βάσεις Δεδομένων και Πληροφοριακά Συστήματα",
            "code_site" : u"HY324",
            "code_eclass": u"MHX311",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX311/",
        }
    }

