
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
        (link, method) = api['pushd.status']
        (page, status_code) = http_request(link, method)

        return True if status_code == 204 else False



class PushdUsers(object):
    def __init__(self, settings, db_manager):
        pass

    def __getitem__(self, key):
        pass

    def register(self, email):
        pass

    def unregister(self):
        pass


class PushdUser(object):
    def __init__(self, settings, db_manager):
        pass

    def subscribe(self):
        pass

    def unsubscribe(self):
        pass

    def update(self):
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


def http_request(link, method, *args, **kargs):
    """
    Makes an http request using requests

    method: 'GET', 'POST', 'PUT', 'DELETE'
    """

    try:
        page = request(method, link, *args, **kargs)
    except requests.exceptions.ConnectionError:
        logger.error('[%s] Connection error exception thrown' % link)
        return None
    except requests.exceptions.Timeout:
        logger.error('[%s] Timeout exception thrown' % link)

    page.encoding = 'utf-8'

    return page

