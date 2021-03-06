from __future__ import absolute_import

import unittest
import os

from uthportal.notifier import PushdClient
from uthportal.configure import Configuration
from uthportal.logger import get_logger
from uthportal.database.memory import MemoryDatabaseManager

class TestPushd(unittest.TestCase):
    def setUp(self):
        self.settings = Configuration().get_settings()
        self.settings['log_dir'] = os.path.abspath("test_logs")
        self.settings['logger']['levels']['notifier'] = 'DEBUG'
        self.db_manager = MemoryDatabaseManager()

        templates = {'very_real_event': {
                                    'title.gr' : 'test',
                                    'msg.gr' : 'this is a message, for real'
                                    }
                    }
        self.pushd = PushdClient(self.settings, self.db_manager, templates)
        self.logger = get_logger('test', self.settings)

    def routine(self):
        self.assertTrue(self.pushd.is_alive())
        user_id = self.pushd.users.register('gcm', 'testtoken123')
        self.assertIsNotNone(user_id)
        #Add user to databse
        self.db_manager.insert_document("users.active",
        {'email' : 'test@uth.gr', 'token': '12345678', 'pushd_id': user_id})
        self.assertTrue('test@uth.gr' in self.pushd.users)

        #try to get user with getter
        pushd_user = self.pushd.users['test@uth.gr']
        self.assertIsNotNone(pushd_user)
        user_info = pushd_user.info()
        self.assertIsNotNone(user_info)
        self.logger.info('User {0}, info: {1}'.format(user_id, str(user_info)))
        #events
        # try to get subscriptiuons before registering anythingg
        subscriptions = pushd_user.get_subscriptions()
        self.assertIsNotNone(subscriptions)
        #register test event
        self.assertTrue(pushd_user.subscribe('very_real_event.testing'))
        subscriptions = pushd_user.get_subscriptions()
        self.assertIsNotNone(subscriptions)
        self.logger.info(subscriptions)

        self.logger.info('getting event info')
        event = self.pushd.events['very_real_event.testing']
        self.assertIsNotNone(event)
        info = event.statistics()
        self.assertIsNotNone(info)
        self.logger.info(info)

        #send event
        self.assertTrue(event.send('example_payload'))

        #unregister user
        self.assertTrue(self.pushd.users.unregister('test@uth.gr'))
    def test_pusd_wrapper(self):
        self.routine()

