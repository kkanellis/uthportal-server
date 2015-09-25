#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests

from logger import get_logger

base_api = {
    'is_alive':               ('/status', 'GET'),
    'users.register' :        ('/subscribers', 'POST'),
    'users.unregister':       ('/subscriber/{pushd_id}', 'DELETE'),
    'users.update':           ('/subscriber/{pushd_id}', 'POST'),
    'user.info':              ('/subscriber/{pushd_id}', 'GET'),
    'user.subscribe':         ('/subscriber/{pushd_id}/subscriptions/{event_name}', 'POST'),
    'user.is_subscribed_to':  ('/subscriber/{pushd_id}/subscriptions/{event_name}', 'GET'),
    'user.unsubscribe':       ('/subscriber/{pushd_id}/subscriptions/{event_name}', 'DELETE'),
    'user.get_subscriptions': ('/subscriber/{pushd_id}/subscriptions', 'GET'),
    'user.set_subscriptions': ('/subscriber/{pushd_id}/subscriptions', 'POST'),
    'event.delete':           ('/event/{event_name}', 'DELETE'),
    'event.statistics':       ('/event/{event_name}', 'GET')
}

api = { }
logger = None

class Pushd(object):
    def __init__(self, settings, db_manager, event_templates):
        global logger

        self.settings = settings
        self.db_manager = db_manager

        logger = get_logger('notifier', settings)

        self.users = PushdUsers(db_manager)
        self.events = PushdEvents(event_templates)

        # Prepend pushd host:port in api urls
        base_url = '%s:%s' % (settings['notifier']['host'], settings['notifier']['port'])
        for (key, value) in base_api.iteritems():
            api[key] = (base_url + value[0], value[1])

    def is_alive(self):
        """
        Returns True if pushd is online and working properly
        """
        (url, method) = api['is_alive']
        response = http_request(url, method)
        if response.status_code == 204:
            return True
        elif response.status_code == 503:
            logger.warn("Pushd can't connect to Redis!")
            return False
        else:
            return False


class PushdUsers(object):
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def __getitem__(self, email):
        pushd_id = self._get_pushd_id(email)

        if pushd_id:
            return PushdUser(pushd_id)
        else:
            err_str = 'User "%s" not found in database' % email
            logger.error(err_str)
            raise KeyError(err_str)

    def register(self, protocol, token, lang='gr', **kwargs):
        """
        Register a new user in pushd

        Return value is 'pushd_id' which must be saved in each user document
        """
        if protocol not in ['gcm', 'wns-toast']:
            logger.error('register: unsupported protocol "%s"' % protocol)
            return None

        # Construct payload
        payload = {
            'proto': protocol,
            'token': token,
            'lang': lang
        }
        payload.update(kwargs)

        (url, method) = api['users.register']

        response = http_request(url, method, data=payload)

        if not response:
            return None

        content = response.json()

        # 200 & 201 status codes are considered valid responses
        if response.status_code == 200:
            _id = content['id']
            logger.debug('User already registered [id=%s]' % _id)
            return _id
        elif response.status_code == 201:
            _id = content['id']
            logger.debug('User successfully registered [id=%s]' % _id)
            return _id

        if response.status_code == 400:
            logger.error('register: Invalid specified token/protocol')
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return None

    def __contains__(self, email):
        """
        Returns True if user is currently registered
        """
        return self.update(email)

    def update(self, email, lang='gr', **kwargs):
        """
        Pings/updates the user to pushd

        This method should be called each time the client app is launched
        """

        pushd_id = self._get_pushd_id(email)
        if not pushd_id:
            return False

        (url, method) = api['users.update']
        url = url.format( pushd_id=pushd_id )

        response = http_request(url, method)

        if not response:
            return False

        if response.status_code == 204:
            logger.debug('[%s]: User info updated successfully' % email)
            return True

        if response.status_code == 400:
            logger.error('Invalid pushd_id/field format')
        elif response.status_code == 404:
            #This is a special case
            #If a 404 is returned, this means that pushd deleted this client\
            #because of inactivity
            #This client has to re-register, in order to recieve notifications
            #TODO: handle this
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
        url = url.format(**{
            'pushd_id': pushd_id
        })

        response = http_request(url, method)

        if not response:
            return False

        if response.status_code == 204:
            logger.debug('User unregistered successfully')
            return True

        if response.status_code == 400:
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
            logger.error('pushd_id not found in "%s" document' % email)
            return None

        return document['pushd_id']

class PushdUser(object):
    def __init__(self, pushd_id):
        if not pushd_id:
            raise ValueError('pushd_id is None')
        self.pushd_id = pushd_id

    def info(self):
        """
        Returns info about the user
        """
        (url, method) = api['user.info']
        url = url.format(**{
            'pushd_id': self.pushd_id
        })

        response = http_request(url, method)

        if not response:
            return None

        if response.status_code == 200:
            return response.json()

        if response.status_code == 400:
            logger.error('Invalid pushd_id format')
        elif response.status_code == 404:
            logger.error('User [id=%s] does not exist' % self.pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return None

    def subscribe(self, event_name, **kwargs):
        """
        Subscribes the user to a notification event
        """
        (url, method) = api['user.subscribe']
        url = url.format(**{
            'pushd_id': self.pushd_id,
            'event_name': event_name
        })
        payload = kwargs

        response = http_request(url, method, data=payload)

        if not response:
            return False

        if response.status_code == 201 or response.status_code == 204:
            logger.debug('Subscribed to "%s" successfully' % event_name)
            return True

        if response.status_code == 400:
            logger.error('Invalid pushd_id/event_name format')
        elif response.status_code == 404:
            logger.error('User [id=%s] does not exist' % self.pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return False


    def is_subscribed_to(self, event_name):
        """
        Returns a list with user subscriptions
        """
        (url, method) = api['user.is_subscribed_to']
        url = url.format( **{
            'pushd_id': self.pushd_id,
            'event_name': event_name
        })

        response = http_request(url, method)

        if not response:
            return None

        if response.status_code == 200:
            return True
        if response.status_code == 404:
            logger.error('User [id=%s] does not exist' % self.pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return False


    def unsubscribe(self, event_name):
        """
        Unsubscribes the user from a notification event
        """
        (url, method) = api['user.unsubscribe']
        url = url.format( **{
            'pushd_id': self.pushd_id,
            'event_name': event_name
        })

        response = http_request(url, method)

        if not response:
            return False

        if response.status_code == 204:
            logger.debug('Unsubscribed from "%s" successfully' % event_name)
            return True

        if response.status_code == 400:
            logger.error('Invalid pushd_id/event_name format')
        elif response.status_code == 404:
            logger.error('User [id=%s] does not exist' % self.pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return False

    def get_subscriptions(self):
        """
        Returns a list with user subscriptions
        """
        (url, method) = api['user.get_subscriptions']
        url = url.format( **{
            'pushd_id': self.pushd_id,
        })

        response = http_request(url, method)

        if not response:
            return None

        if response.status_code == 200:
            logger.debug('Recieved subscriptions for "%s"' % self.pushd_id)
            events_dict = response.json()
            return [ event_name for (event_name, _) in events_dict.iteritems() ]

        if response.status_code == 404:
            logger.error('User [id=%s] does not exist' % self.pushd_id)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return None


    def set_subscriptions(self, events):
        # TODO
        pass

class PushdEvents(object):
    def __init__(self, event_templates):
        for key in event_templates.keys():
            template = event_templates[key]
            if ('title' not in template or 'msg' not in template):
                err_str = ' "title" and/or "msg" are missing from "%s" template' % template
                logger.error(err_str)
                raise ValueError(err_str)
        self.templates = event_templates

    def __getitem__(self, event_name):
        collection = self.__get_collection(event_name)

        if collection in self.templates:
            template = self.templates[collection]
            return PushdEvent(event_name, template)
        else:
            raise KeyError('No valid template found for this event: ' + event_name)

    def __delitem__(self, event_name):
        (url, method) = api['events.delete']
        url = url.format( {'event_name': event_name })

        response = http_request(url, method)

        if not response:
            logger.warning('Failed to remove [%s], No response' % event_name)

        if response.status_code == 204:
            logger.debug('Event [%s] successfully deleted' % event_name)
        elif response.status_code == 404:
            err_str = 'Event [%s] does not exist' % event_name
            logger.error(err_str)
            raise KeyError(err_str)
        else:
            logger.error('Request returned [%s]' % response.status_code)


    def __contains__(self, event_name):
        return True if self.__get_collection(event_name) in self.templates.keys() else False

    def __get_collection(self, fullpath):
        dot_parts = fullpath.split('.')
        return '.'.join(dot_parts[::-1])

class PushdEvent(object):
    def __init__(self, event_name, template):
        self.name = name
        self.template = template

    def statistics(self):
        if not self.name:
            return None

        (url, method) = api['user.statistics']
        url = url.format( **{
            'event_name': self.name
        })

        response = http_request(url, method)

        if not response:
            return None

        if response.status_code == 200:
            logger.debug('Statistics returned')
            return response.json()

        if response.status_code == 404:
            logger.warning('Event [%s] does not exist' % event_name)
        else:
            logger.error('Request returned [%s]' % response.status_code)

        return None

    def send(self, data=None, var=None):
        if not self.name:
            return False

        if not data or not var:
            logger.error('Empty data and/or var dicts')
            return False

        (url, method) = api['user.send']
        url = url.format( {'event_name': self.name})

        response = http_request(url, method)

        if not response:
            return False

        if response.status_code == 204:
            # We can't be sure push notifications are delivered
            # 204 means only that pushd will handle the request
            logger.debug('Event will be send')
            return True
        else:
            logger.error('Request returned [%s]' % response.status_code)
            return False


def http_request(url, method, *args, **kwargs):
    """
    Makes an http request using requests

    method: 'GET', 'POST', 'PUT', 'DELETE'
    """
    if not url.startswith('http://'):
        url = 'http://' + url

    try:
        logger.debug('Making %s request @ %s', method, url)
        page = requests.request(method, url, *args, **kwargs)
    except requests.exceptions.ConnectionError:
        logger.error('[%s] Connection error exception thrown' % url)
        return None
    except requests.exceptions.Timeout:
        logger.error('[%s] Timeout exception thrown' % url)
        return None
    except Exception as e:
        logger.error(e)
        return None

    page.encoding = 'utf-8'
    return page
