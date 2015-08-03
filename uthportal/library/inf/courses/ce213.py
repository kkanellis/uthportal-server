#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from uthportal.tasks.course import CourseTask

class ce213(CourseTask):
    document_prototype = {
        'code': 'ce213',
        'announcements': {
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE213/news.html',
            'link_eclass': ''
        },
        'info': {
            'name': u'Αριθμητική Ανάλυση',
            'code_site': u'HY213',
            'code_eclass': '',
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE213/',
            'link_eclass': ''
        }
    }

    def parse_site(self, bsoup):
        """
        HTML Format:

        <li>
           <h3> <font color="#669933">date1. </font></h3>
            <p> html1
            </p>
        </li>

        <li>
           <h3> <font color="#669933">date2. </font></h3>
           <p> html2
           </p>
        </li>
        ....
        """
        # Find all html announcement
        htmls = bsoup.select('li h3 ~ p')

        # Find all dates
        dates = bsoup.select('li h3 > font')
        dates = [ datetime.strptime(date.text.strip(' .').replace('.','/'), '%d/%m/%Y')
                    for date in dates ]

        return [{   'date': date,
                    'html': unicode(html),
                    'has_time': False,
                    'plaintext': html.text.strip()
                    } for (date, html) in zip(dates, htmls) ]

