#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from uthportal.tasks.course import CourseTask

class ce121(CourseTask):
    entry = {
        'code': 'ce121',
        'code_eclass': '',
        'announcements': {
            'link_site':'http://inf-server.inf.uth.gr/courses/CE121/',
            'link_eclass': ''
        },
        'info': {
            'name': u'Προγραμματισμός II',
            'link_site': 'http://inf-server.inf.uth.gr/courses/CE121/',
            'link_eclass': ''
        }
    }

    def parse_site(self, bsoup):
        """
        <a id="announce"></a>
        <h3>Ανακοινωσεις</h3>
        <ul class="nb">
            <li><b>date1 <span style="color:#C00000"> title1 </span> </b><br>
                <ul class="nb">
                    <li> html1
                    </li>
                </ul>
            </li>
            <li><b>date2 <span style="color:#C00000"> title2 </span> </b><br>
                <ul class="nb">
                    <li> html2
                    </li>
                </ul>
            </li>
        </ul>
        """
        # Get the region of the announcements
        announce_region = bsoup.find('a', id='announce')

        # Move to the ul tag
        announce_region = announce_region.find_next_sibling()
        announce_region = announce_region.find_next_sibling()

        # Find all b inside li (dates & titles)
        dates_titles = announce_region.select('li > b')

        # Find all announcements html
        htmls = announce_region.find_all('ul', class_='nb')

        # Remove the ul 'outer' tag and create the plaintext entry
        plaintexts = [ ]
        for (i, html) in enumerate(htmls):
            plaintexts.append(html.text.strip())
            html = unicode(html).replace('<ul class="nb">', '')
            html = unicode(html).replace('</ul>', '')
            htmls[i] = html

        # Create the final list
        announce_list = [ {'title': element.span.extract().text.encode('utf8'), \
                            'date': datetime.strptime(element.text.strip(), '%d/%m/%Y'), 'has_time': False, \
                            'html': htmls[i].encode('utf8').strip(), \
                            'plaintext': plaintexts[i] } for (i, element) in enumerate(dates_titles) ]

        return announce_list

