#!/usr/bin/python
# -*- coding: utf8 -*-

import os.path

from uthportal.tasks.static import StaticTask

class curriculum(StaticTask):
    filename = 'curriculum.html'
    filedir = os.path.dirname(__file__)

    document_prototype = {
        'type': 'curriculum',
        'entries': [ ]
    }

    def parse(self, bsoup):
        # Find all divs (for all 5 days of the week)
        divs = bsoup.find_all('div', class_='tab_content')

        # days = [ u'Δευτέρα', u'Τρίτη', u'Τετάρτη', u'Πέμπτη', u'Παρασκευή' ]
        cell_key = ['timespan', 'course_name', 'class_type', 'classroom', 'instructor' ]
        curriculum = [ ]
        for (day, cc) in enumerate(divs):
            rows = cc.find_all('tr') # Split to rows
            for row in rows:
                # Contructing entry
                entry = {
                    cell_key[index] : cell.text
                    for index, cell in enumerate(row.find_all('td'))
                }

                # Check if valid entry
                if not entry:
                    continue

                # Special parsing for time (start_time, end_time)
                entry['start_time'], entry['end_time'] = entry['timespan'].split(u'–')
                del entry['timespan']

                # Stripping whitespaces & adding day
                entry = { key: value.strip() for key, value in entry.iteritems() }
                entry['day'] = day

                curriculum.append(entry)

        return curriculum


