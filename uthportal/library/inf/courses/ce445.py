#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.course import CourseTask

class ce445(CourseTask):
    document_prototype = {
        "code": "ce445",
        "announcements": {
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX319"
        },
        "info": {
            "name": u"Ασύρματες Επικοινωνίες",
            "code_site": u"HY445",
            "code_eclass": "MHX319",
            "link_site": "",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX319/"
        }
    }

