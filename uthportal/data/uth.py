#!/usr/bin/env python
# -*- coding: utf-8 -*-

### uth.rss ############################################

uth_rss = { }
uth_rss_suffix = '?format=feed&type=rss'

uth_rss['news'] = {
    'type': 'news',
    'link': 'http://uth.gr/news',
    'link_suffix': uth_rss_suffix,
    'title': u'Νέα Πανεπιστημίου Θεσσαλίας',
    'entries': [ ],
}

uth_rss['events'] = {
    'type': 'events',
    'link': 'http://uth.gr/events',
    'link_suffix': uth_rss_suffix,
    'title': u'Προσεχείς Εκδηλώσεις Π.Θ',
    'entries': [ ],
}

uth_rss['genannounce'] = {
    'type': 'genannounce',
    'link': 'http://uth.gr/genannounce',
    'link_suffix': uth_rss_suffix,
    'title': u'Γενικές Ανακοινώσεις Π.Θ',
    'entries': [ ],
}

