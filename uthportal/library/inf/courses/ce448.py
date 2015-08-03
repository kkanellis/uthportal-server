#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce448(CourseTask):
    document_prototype = {
            "code": "ce448",
            "announcements": {
                "link_site": "",
                "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX313"
            },
            "info": {
                "name": u"Προχωρημένα Θέματα Δικτύων",
                "code_site": u"HY448",
                "code_eclass": "MHX313",
                "link_site": "",
                "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX313/"
            }
        }

