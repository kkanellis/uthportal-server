#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests

from logger import get_logger

api = {
    'pushd.is_alive':         ('/status', 'GET'),
    'users.register' :        ('/subscribers', 'POST'),
    'users.unregister':       ('/subscribers/{pushd_id}', 'DELETE'),
    'users.update':           ('/subscribers/{pushd_id}', 'POST'),
    'user.info':              ('/subscribers/(pushd_id}', 'GET'),
    'user.subscribe':         ('/subscriber/{pushd_id}/subscriptions/{event_id}', 'POST'),
    'user.unsubscribe':       ('/subscriber/{pushd_id}/subscriptions/{event_id}', 'DELETE'),
    'user.get_subscriptions': ('/subscriber/{pushd_id}/subscriptions', 'GET'),
    'user.set_subscriptions': ('/subscriber/{pushd_id}/subscriptions', 'POST')
}

logger = None

class PushdWrapper(object):

    def __init__(self, settings, db_manager):
        global logger

        self.settings = settings
        self.db_manager = db_manager

        logger = get_logger('notifier', settings)

        self.users = PushdUsers(db_manager)
        self.events = PushdEvents(db_manager)

        # Prepend pushd host:port in api urls
        base_url = '%s:%s' % (settings['notifier']['host'], settings['notifier']['port'])
        for (key, value) in api.iteritems():
            api[key] = base_url + value

    def is_alive(self):
        """
        Returns True if pushd is online and working properly
        """
        (url, method) = api['pushd.is_alive']
        response = http_request(url, method)

        return True if response.status_code == 204 else False


class PushdUsers(object):
    def __init__(self, db_manager):
        self.settings = settings
        self.db_manager = db_manager

    def __getitem__(self, email):
        pushd_id = self._get_pushd_id(email)

        if pushd_id:
            return PushdUser(pushd_id)
        else:
            logger.error('User "%s" not found in database' % email)
            return PushdUser(None)

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

        content = json.loads( response.json() )

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

    def exists(self, email):
        """
        Returns True if user is currently registered
        """
        pass

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
    def __init__(self, pushd_id):
        self.pushd_id = push_id

    def info(self):
        """
        Returns info about the user
        """

        if not self.pushd_id:
            return None

        (url, method) = api['user.info']
        url = url.format( {'pushd_id': self.pushd_id} )

        logger.debug('Making %s request @%s', method, url)
        response = http_request(url, method)

        if response.status_code == 200:
            logger.debug('User exists! Returning info')
            return json.loads( response.json() )

        if response.status_code == 400:
            logger.error('Invalid pushd_id format')
        elif response.status_code == 404:
            logger.error('User [id=%s] does not exist' % self.pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return None

    def subscribe(self, event_id, **kwargs):
        """
        Subscribes the user to a notification event
        """

        if not self.pushd_id:
            return None

        (url, method) = api['user.subscribe']
        url = url.format( {
            'pushd_id': self.pushd_id,
            'event_id': event_id
        })

        payload = { }
        payload.update(kwargs)

        logger.debug('Making %s request @%s', method, url)
        response = http_request(url, method, params=payload)

        if response.status_code == 201 or response.status_code == 204:
            logger.debug('Subscribed to "%s" successfully' % event_id)
            return True

        if response.status_code == 400:
            logger.error('Invalid pushd_id/event_id format')
        elif response.status_code == 404:
            logger.error('User [id=%s] does not exist' % self.pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return False

    def unsubscribe(self):
        """
        Unsubscribes the user from a notification event
        """

        if self.pushd_id:
            return None

        (url, method) = api['user.unsubscribe']
        url = url.format( {
            'pushd_id': self.pushd_id,
            'event_id': event_id
        })

        logger.debug('Making %s request @%s', method, url)
        response = http_request(url, method)

        if response.status_code == 204:
            logger.debug('Unsubscribed from "%s" successfully' % event_id)
            return True

        if response.status_code == 400:
            logger.error('Invalid pushd_id/event_id format')
        elif response.status_code == 404:
            logger.error('User [id=%s] does not exist' % self.pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return False

    def get_subscriptions(self):
        """
        Returns a list with user subscriptions
        """

        if self.pushd_id:
            return None

        (url, method) = api['user.get_subscriptions']
        url = url.format( {
            'pushd_id': self.pushd_id,
        })

        logger.debug('Making %s request @%s', method, url)
        response = http_request(url, method)

        if response.status_code == 200:
            logger.debug('Recieved subscriptions for "%s"' % self.pushd_id)
            events_dict = json.loads( response.json() )
            return [ event_id for (event_id, _) in events_dict.iteritems() ]

        if response.status_code == 404:
            logger.error('User [id=%s] does not exist' % self.pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return None

    def set_subscriptions(self, events):
        pass

class PushdEvents(object):
    def __init__(self, db_manager):
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

