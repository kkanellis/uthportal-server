#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ee355(CourseTask):
    document_prototype = {
        "code": "ee355",
        "code_eclass": u"INFS126",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=INFS126"
        },
        "info": {
            "name": u"Εφαρμοσμένη Θερμοδυναμική",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/INFS126/"
        }
    }

