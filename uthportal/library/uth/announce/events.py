#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.rss_announcement import RssAnnouncementTask

class events(RssAnnouncementTask):
    document_prototype = {
        'type': 'events',
        'link': 'http://www.uth.gr/events?format=feed&type=rss'
    }

