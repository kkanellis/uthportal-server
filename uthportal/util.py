#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from time import mktime
from datetime import datetime
from urlparse import urljoin, urlparse
from json import JSONEncoder

import requests
import feedparser
from bs4 import BeautifulSoup

FOOD_MENU_PAGE = 'http://www.uth.gr/students/student-welfare/programma-sitisis'

VLL_TEXT = 'ΒΟΛΟΣ, ΛΑΡΙΣΑ, ΛΑΜΙΑ'
TK_TEXT = 'ΤΡΙΚΑΛΑ, ΚΑΡΔΙΤΣΑ'


class BSONEncoderEx(JSONEncoder):
    """
    Extending JSONEncoder to support datetime & ObjectId (mongo-id) objects
    when using python's json library
    """
    def default(self, obj, **kwargs):
        from bson.objectid import ObjectId
        from datetime import datetime

        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return JSONEncoder.default(self, obj, **kwargs)

def is_equal(a, b):
    a = str(a)
    b = str(b)
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0

def get_first_n_digits(integer, digits):
    import math
    digits -= 1
    while int(math.log10(abs(integer))) >  digits:
        integer /= 10

    return int(integer)

def truncate_str(data, length):
    length -= 2
    return (data[:length] + '...') if len(data) > length else data

def fix_urls(html, base_link):
    bsoup = BeautifulSoup(html)

    for a_tag in bsoup.find_all('a'):
        # Check for relative link
        if a_tag.has_attr('href') and not urlparse(a_tag['href']).netloc:
            a_tag['href'] = urljoin(base_link, a_tag['href'])

    return unicode(bsoup)

def download_file(link, filename, timeout=5.0):
    """
    Download a file and save it to disk
    """
    #check if directory exists and create if needed
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'wb') as f:
        try:
            # streaming the file to its location
            page = requests.get(link, timeout=timeout, stream=True)
            if page.status_code is not (200 or 301):
                return False

            for block in page.iter_content():
                f.write(block)

        except requests.exceptions.Timeout:
            logger.warning("download_file: timeout while fetching" + '\n\t' + link)
            return False

    return True

def get_soup(html):
    """ Returns the BeautifulSoup object from the html """
    bsoup = None
    try:
        bsoup = BeautifulSoup(html, 'html5lib')
    except Exception as e:
        #Find a solution for this
        print('Error while parsing html: %s' % e)

    return bsoup


def get_raw_webpage(url):
    """
    Download a web url as raw bytes
    """
    page = requests.get(url)
    if page.status_code is not (200 or 301):
        return False

    return page.text


def get_food_links():
    food_links = {
            'vll' : [],
            'tk' : []
    }

    html = get_raw_webpage(FOOD_MENU_PAGE)
    soup = get_soup(html)

    all_p = soup.find_all('p')
    for par in all_p:
        if par is not None:
            if VLL_TEXT in str(par):
                for child in par.findChildren('a', href=True):
                    food_links['vll'].append(child['href'])

            if TK_TEXT in str(par):
                for child in par.findChildren('a', href=True):
                    food_links['tk'].append(child['href'])

    return food_links


def parse_rss(html):
    """
    Returns a list of entries for the given RSS in HTML format
    """

    rss = feedparser.parse(html)
    # Datetime format
    # dt_format = '%a, %d %b %Y %H:%M:%S %z'
    entries = [{
                'title': entry.title,
                'html': entry.description,
                'plaintext': get_soup(entry.description).text,
                'link': entry.link,
                'date': datetime.fromtimestamp(mktime(entry.published_parsed)),
                'has_time': True
                }
                for entry in rss.entries ]

    return sorted(entries, key=lambda entry: entry['date'].isoformat())[::-1]

def date_to_datetime(date):
    """
    Converts date object to datetime, supported by MongoDB
    """
    return datetime.combine(date, datetime.min.time() )


def parse_greek_date(date_str):
    '''
    Parses a unicode string that containts a greek date into a
    datetime object
    '''
    replacer = {
            u'Ιαν': 'Jan',
            u'Φεβ': 'Feb',
            u'Μαρ': 'Mar',
            u'Απρ': 'Apr',
            u'Μάι': 'May',
            u'Ιουν': 'Jun',
            u'Ιουλ': 'Jul',
            u'Αυγ': 'Aug',
            u'Σεπ': 'Sep',
            u'Οκτ': 'Oct',
            u'Νοε': 'Nov',
            u'Δεκ': 'Dec'
    }

    date_str = date_str.strip()
    for (date_gr, date_en) in replacer.items():
        date_str = date_str.replace(date_gr, date_en)

    return datetime.strptime(date_str, '%d %b, %Y')
