#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.announcement import AnnouncementTask
from uthportal.util import parse_rss

class RssAnnouncementTask(AnnouncementTask):
    def parse(self, bsoup):
        return parse_rss(unicode(bsoup))

