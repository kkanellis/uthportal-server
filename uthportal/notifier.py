#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from logger import get_logger

api = {
    'pushd.is_alive':         ('/status', 'GET'),
    'users.register' :        ('/subscribers', 'POST'),
    'users.unregister':       ('/subscribers/{pushd_id}', 'DELETE'),
    'users.update':           ('/subscribers/{pushd_id}', 'POST'),
    'user.subscribe':         ('/subscriber/{pushd_id}/subscriptions/{event_id}', 'POST'),
    'user.unsubscribe':       ('/subscriber/{pushd_id}/subscriptions/{event_id}', 'DELETE'),
    'user.get_subscriptions': ('/subscriber/{pushd_id}/subscriptions', 'GET')
}

logger = None

class PushdWrapper(object):

    def __init__(self, settings, db_manager):
        global logger

        self.settings = settings
        self.db_manager = db_manager

        logger = get_logger('notifier', settings)

        self.users = PushdUsers(settings, db_manager)
        self.events = PushdEvents(settings, db_manager)

        # Prepend pushd host:port in api urls
        base_url = '%s:%s' % (settings['notifier']['host'], settings['notifier']['port'])
        for (key, value) in api.iteritems():
            api[key] = base_url + value

    def is_alive(self):
        """
        Returns True if pushd is online and working properly
        """
        (url, method) = api['pushd.status']
        response = http_request(url, method)

        return True if response.status_code == 204 else False


class PushdUsers(object):
    def __init__(self, settings, db_manager):
        self.settings = settings
        self.db_manager = db_manager

    def __getitem__(self, email):
        pushd_id = self._get_pushd_id(email)

        if pushd_id:
            return PushdUser(self.settings, self.db_manager, pushd_id)
        else:
            logger.error('User "%s" not found in database' % email)
            return None

    def register(self, protocol, token, lang='el-gr', **kwargs):
        """
        Register a new user in pushd

        Return value is 'pushd_id' which must be saved in each user document
        """
        if protocol not in ['gcm', 'mpns', 'wns']:
            logger.error('register: unsupported protocol "%s"' % protocol)
            return None

        # Construct payload
        payload = {
            'proto': protocol,
            'token': token,
            'lang': lang
        }
        payload.update(kwargs)

        # Make the request
        (url, method) = api['users.register']

        logger.debug('Making %s request @%s', method, url)
        response = http_request(url, method, params=payload)

        content = response.json()

        # 200 & 201 status codes are considered valid responses
        if response.status_code == 200:
            logger.debug('User already registered [id=%s]')
            return content['id']
        elif response.status_code == 201:
            logger.debug('User successfull registered [id=%s]')
            return content['id']
        elif response.status_code == 400:
            logger.error('register: Invalid specified token/protocol')
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return None

    def update(self, email, lang='el-gr', **kwargs):
        """
        Pings/updates the user to pushd

        This method should be call each time the client app is launched
        """

        pushd_id = self._get_pushd_id(email)

        if not pushd_id:
            return False

        (url, method) = api['users.update']
        url = url.format( {'pushd_id': pushd_id} )

        logger.debug('Making %s request @%s', method, url)
        response = http_request(url, method)

        if response.status_code == 204:
            logger.debug('User info edited successfully')
            return True

        if response.status_code == 400:
            logger.error('Invalid pushd_id/field format')
        elif response.status_code == 404:
            logger.error('User not found [id=%s]' % pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return False


    def unregister(self, email):
        """
        Unregisters a user from pushd

        Returns True/False
        """
        pushd_id = self._get_pushd_id(email)

        if not pushd_id:
            return False

        (url, method) = api['users.unregister']
        url = url.format( {'pushd_id': pushd_id} )

        logger.debug('Making %s request @%s', method, url)
        response = http_request(url, method)

        if response.status_code == 204:
            logger.debug('User unregistered successfully')
            return True
        elif response.status_code == 400:
            logger.error('Invalid pushd_id format [id=%s]' % pushd_id)
        elif response.status_code == 404:
            logger.error('User not found [id=%s]' % pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return False

    def _get_pushd_id(self, email):
        query = { 'email': email }
        document = self.db_manager.find_document('users.active', query)

        if not document:
            logger.error('User "%s" not found in database' % email)
            return None

        if 'pushd_id' not in document:
            logger.error('Pushd_id not found for "%s"' % email)
            return None

        return document['pushd_id']

class PushdUser(object):
    def __init__(self, settings, db_manager, pushd_id):
        pass

    def subscribe(self):
        pass

    def unsubscribe(self):
        pass

    def get_subscriptions(self):
        pass

class PushdEvents(object):
    def __init__(self, settings):
        pass

    def __getitem__(self, key):
        pass

    def add(self):
        pass

    def delete(self):
        pass

    def get_statistics(self):
        pass


def http_request(url, method, *args, **kwargs):
    """
    Makes an http request using requests

    method: 'GET', 'POST', 'PUT', 'DELETE'
    """

    try:
        page = request(method, url, *args, **kwargs)
    except requests.exceptions.ConnectionError:
        logger.error('[%s] Connection error exception thrown' % url)
        return None
    except requests.exceptions.Timeout:
        logger.error('[%s] Timeout exception thrown' % url)

    page.encoding = 'utf-8'
    return page

