#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from uthportal.tasks.course import CourseTask


def parse(bsoup):
    # create a list of the announcement dates
    dates_raw = [ date.find('b').text.strip() for date in bsoup.find_all('dt') ]
    dates = [ datetime.strptime(date, '%d/%m/%Y') for date in dates_raw ]

    contents = []
    plaintexts = []

    # create a list of the announcement html contents
    dd_contents = bsoup.find_all('dd')
    for dd_elements in dd_contents:
        content = u''
        plaintext = u''
        for element in dd_elements:
            content += unicode(element)

            if hasattr(element, 'text'):
                plaintext += element.text
            else:
                plaintext += unicode(element)

        contents.append( content.strip() )
        plaintexts.append( plaintext )

    # return the date/content tuples
    return [{  'date':date,
                'html':html,
                'plaintext': plaintext,
                'has_time': False
            } for (date, html, plaintext) in zip(dates, contents, plaintexts) ]

class ce232(CourseTask):
    document_prototype = {
        'code': 'ce232',
        'announcements': {
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE232/',
            'link_eclass': ''
        },
        'info': {
            'name': u'Οργάνωση και Σχεδίαση Η/Υ',
            'code_site': 'HY232',
            'code_eclass': '',
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE232/',
            'link_eclass': ''
        }
    }

    def parse_site(self, bsoup):
        return parse(bsoup)

