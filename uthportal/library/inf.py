#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" library/inf.py: Contains all special functions needed for inf dept

Currently contains DOM parsers, designed to retrieve announcements from
specialized courses' sites. Each function is named afer the course code
and its job is to convert the DOM object (specifically BeautifulSoup)
to an array of dictionaries, which have the following format:

    html: HTML format of the announcement
    plaintext: Announcement without any formatting
    date: date(time) announced
    link: Hyperlink to the announcement
    has_time: designates whether or not time is present in date field

"""

