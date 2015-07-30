#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

import requests
from bs4 import BeautifulSoup

from uthportal.configure import Contructing

HTML_PATH = 'curriculum.html'

def parse(html):

    bsoup = BeautifulSoup(html)

    # Find all divs (for all 5 days of the week)
    divs = bsoup.find_all('div', class_='tab_content')

    days = [ u'Δευτέρα', u'Τρίτη', u'Τετάρτη', u'Πέμπτη', u'Παρασκευή' ]
    cell_key = ['timespan', 'course_name', 'class_type', 'classroom', 'instructor' ]
    curriculum = [ ]
    for (day, cc) in enumerate(divs):
        rows = cc.find_all('tr') # Split to rows
        for row in rows:
            print row
            # Contructing entry
            entry = {
                cell_key[index] : cell.text
                for index, cell in enumerate(row.find_all('td'))
            }

            # Check if valid entry
            if not entry:
                continue

            entry['day'] = days[day]

            # Special parsing for time (start_time, end_time)
            entry['start_time'], entry['end_time'] = entry['timespan'].split(u'–')
            del entry['timespan']

            # Stripping whitespaces
            entry = { key: value.strip() for key, value in entry.iteritems() }

            curriculum.append(entry)

    return curriculum


def main():

    # Read html file contents
    try:
        with open(HTML_PATH, 'r') as f:
            html = f.read().decode('utf8')
    except IOError as e:
        print 'Cannot read from "%s". Please make sure the file exists' % HTML_PATH
        return

    try:
        curriculum = parse(html)
    except Exception as e:
        print 'Exception: %s' % e
        return


    data = json.dumps(
                curriculum,
                ensure_ascii=False,
                indent=4
            )

    print data


if __name__ == '__main__':
    main()
