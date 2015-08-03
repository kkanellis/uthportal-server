#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce322(CourseTask):
    document_prototype = {
        "code": "ce322",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX317"
        },
        "info": {
            "name": u"Τεχνητή Νοημοσύνη",
            "code_site": u"HY322",
            "code_eclass": u"MHX317",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX317/"
        }
    }

