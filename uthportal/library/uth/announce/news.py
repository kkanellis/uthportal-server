#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.rss_announcement import RssAnnouncementTask

class news(RssAnnouncementTask):
    document_prototype = {
        'type': 'news',
        'link': 'http://www.uth.gr/news?format=feed&type=rss'
    }

