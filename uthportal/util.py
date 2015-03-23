from urlparse import urljoin, urlparse

from bs4 import BeautifulSoup

from uthportal.logger import get_logger, logging_level

logger = get_logger(__name__, logging_level.DEBUG)

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
            logger.error('Error while parsing html: %s' % e)

        return bsoup

