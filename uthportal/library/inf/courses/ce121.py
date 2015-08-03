#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from uthportal.tasks.course import CourseTask
from datetime import datetime

class ce121(CourseTask):
    document_prototype = {
        'code': 'ce121',
        'announcements': {
            'link_site':'http://inf-server.inf.uth.gr/courses/CE121/',
            'link_eclass': ''
        },
        'info': {
            'name': u'Προγραμματισμός II',
            'code_site': 'HY121',
            'code_eclass': '',
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
        info_region = bsoup.find('a', id='info')

        #get titels & htmls
        dates_titles = []
        htmls = []
        for sibling in  announce_region.next_siblings:
            if sibling.name == 'h5':
                dates_titles.append(sibling)
            if sibling.name == 'ul':
                htmls.append(sibling)
            if sibling is info_region:
                break

        # Remove the ul 'outer' tag and create the plaintext entry
        plaintexts = [ ]
        for (i, html) in enumerate(htmls):
            plaintexts.append(html.text.strip())
            html = unicode(html).replace('<ul class="nb">', '')
            html = unicode(html).replace('</ul>', '')
            htmls[i] = html

        # Create the final list
        announce_list = [ {'title': element.span.extract().text,
                            'date': datetime.strptime(element.text.strip(), '%d/%m/%Y'),
                            'html': unicode(htmls[i]).strip(),
                            'plaintext': plaintexts[i],
                            'has_time': False }
                                for (i, element) in enumerate(dates_titles)]

        return announce_list

