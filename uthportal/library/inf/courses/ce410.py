#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from uthportal.tasks.course import CourseTask

def parse(bsoup):
    """
    <div class="body_resize">
        <div class="left"
            ...
            <h4>
                date1
            </h4>
            <p>
                html1
            </p>
            <h4>
                date2
            </h4>
            <p>
                html2
            </p>
            ...
        />
    />
    """
    announce_region = bsoup.find('div', class_='body_resize').find('div', class_='left')

    dates = announce_region.find_all('h4')
    dates = [ datetime.strptime( date.text.strip(' .').replace('.', '/'), '%d/%m/%Y')
                for date in dates ]

    htmls = announce_region.find_all('p')[:len(dates)]

    return [{
                'date': date,
                'html': unicode(html),
                'has_time': False,
                'plaintext': html.text.strip()
            } for (date, html) in zip(dates, htmls)]


class ce410(CourseTask):
    document_prototype = {
        "code": "ce410",
        "announcements": {
            "link_site": "http://inf-server.inf.uth.gr/courses/CE410/news.html",
            "link_eclass": "http://eclass.uth.gr/eclass/modules/announcements/rss.php?c=MHX251"
        },
        "info": {
            "name": u"Παράλληλοι και Δικτυακοί Υπολογισμοί",
            "code_site": "HY410",
            "code_eclass": "MHX251",
            "link_site": "http://inf-server.inf.uth.gr/courses/CE410/",
            "link_eclass": "http://eclass.uth.gr/eclass/courses/MHX251/"
        }
    }

    def parse_site(self, bsoup):
        return parse(bsoup)

