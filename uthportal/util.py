# -*- coding: utf-8 -*-
from datetime import datetime
from urlparse import urljoin, urlparse

from bs4 import BeautifulSoup

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

def get_soup(html):
        """ Returns the BeautifulSoup object from the html """
        bsoup = None
        try:
            bsoup = BeautifulSoup(html)
        except Exception, e:
            #Find a solution for this
            print('Error while parsing html: %s' % e)

        return bsoup

def parse_greek_date(date_str):
    '''
    Parses a unicode string that containts a greek date into a
    datetime object
    '''

    date_str = date_str.strip()
    date_str = date_str.replace( u'Ιαν', 'Jan' )
    date_str = date_str.replace( u'Φεβ', 'Feb' )
    date_str = date_str.replace( u'Μαρ', 'Mar' )
    date_str = date_str.replace( u'Απρ', 'Apr' )
    date_str = date_str.replace( u'Μάι', 'May' )
    date_str = date_str.replace( u'Ιουν', 'Jun' )
    date_str = date_str.replace( u'Ιουλ', 'Jul' )
    date_str = date_str.replace( u'Αυγ', 'Aug' )
    date_str = date_str.replace( u'Σεπ', 'Sep' )
    date_str = date_str.replace( u'Οκτ', 'Oct' )
    date_str = date_str.replace( u'Νοε', 'Nov' )
    date_str = date_str.replace( u'Δεκ', 'Dec' )

    return datetime.strptime(date_str, '%d %b, %Y')