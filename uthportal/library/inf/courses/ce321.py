#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import punctuation
from datetime import datetime

from uthportal.tasks.course import CourseTask

class ce321(CourseTask):
    document_prototype = {
        'code': 'ce321',
        'code_eclass': '',
        'announcements': {
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE321/',
            'link_eclass': ''
        },
        'info': {
            'name': u'Λειτουργικά Συστήματα',
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE321/',
            'link_eclass': ''
        }
    }

    def parse_site(self, bsoup):
        """
        course: ce321 : Λειτουργικα Συστηματα
        HTML format:
        <span class="date"> #date1# </span> #announce1#
        <span class="date"> #date2# </span> #announce2#
        ...
        """

        announce_list = [ ]
        for announce in bsoup.find_all('span', 'color:#'):
            # Get date, remove any unwanted punctuation and convert to datetime
            date_string = announce.text.strip(punctuation)
            date = datetime.strptime(date_string, '%d/%m/%Y')

            html = u''
            plaintext = u''

            # Get the parts of the announcement
            for element in announce.next_sibling:
                html += unicode(element)

                if hasattr(element, 'text'):
                    plaintext += element.text.strip()
                else:
                    plaintext += unicode(element)

            # Add the new announcement as dictionary
            announce_list.append( {
                'date': date,
                'html': html,
                'plaintext': plaintext,
                'has_time': False } )

        # Return the list of announcements
        return announce_list

