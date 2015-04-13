#/usr/bin/env python
# -*- coding: utf-8 -*-

"""
List of methods used for authentication of scrapping modules
"""

from requests.exceptions import ConnectionError, Timeout

def https_post(session, link, payload):
    """ Makes an https POST request """
    try:
        response = session.post(link, verify=False, data=payload)
    except ConnectionError:
        self.logger.warning('%s: Connection error' % link)
        return None
    except Timeout:
        self.logger.warning('%s: Timeout [%d]' % (link, self.timeout))
        return None

    if response.status_code is not (200 or 301):
        self.logger.warning('%s: Returned [%d]' % (link, page.code))

    return response

