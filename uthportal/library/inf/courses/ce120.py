#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import punctuation
from datetime import datetime

from uthportal.tasks.course import CourseTask

class ce120(CourseTask):
    document_prototype = {
        'code': 'ce120',
        'code_eclass': '',
        'announcements': {
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE120/',
            'link_eclass': ''
        },
        'info': {
            'name': u'Προγραμματισμός I',
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE120/',
            'link_eclass': ''
        }
    }

    def parse_site(self, bsoup):
        """
        course: ce120 : Προγραμματισμός 1

        HTML format:
            <div class="announce">
                <p>
                <span class="date"> #date1# </span> #announce1#
                </p>
                <p>
                <span class="date"> #date2# </span> #announce2#
                </p>
                ...
            </div>
        """

        # find the 'announce' class which contains the announcements
        # bsoup.find(tag_name, attributes)
        announce_class = bsoup.find('div', class_ = 'announce')

        # Initialize an empty list
        announce_list = []

        # Parse each announcement
        for announce in announce_class.find_all('span', class_ = 'date'):
            # Get date, remove any unwanted punctuation and convert to datetime
            # Formats: http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
            date_string = announce.text.strip(punctuation)
            date = datetime.strptime(date_string , '%d/%m/%Y')

            # Get the parts of the announcement
            html_parts = []
            plaintext_parts = []
            for part in announce.next_siblings:
                if part.name is 'span' or part.name is 'p':
                    break

                part_u = unicode(part).strip()
                html_parts.append(part_u)
                if hasattr(part, 'text'):
                    plaintext_parts.append(part.text.strip())
                else:
                    plaintext_parts.append(part_u)

            # convert list to unicode
            html = (u' '.join( html_parts )).strip()
            plaintext = (u' '.join( plaintext_parts )).strip()

            # Add the new announcement as dictionary
            announce_list.append( {'date':date, 'html':html, 'plaintext': plaintext, 'has_time': False } )

        # Return the list of announcements
        return announce_list

