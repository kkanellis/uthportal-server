#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce340(CourseTask):
    document_prototype = {
        "code": "ce340",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX310"
        },
        "info": {
            "name": "Δίκτυα Υπολογιστών Ι",
            "code_site": u"HY340",
            "code_eclass": "MHX310",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX310/"
        }
    }

