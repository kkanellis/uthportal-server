from __future__ import absolute_import

import unittest
import os

from uthportal.notifier import Pushd
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
                                    'title' : 'test',
                                    'msg' : 'this is a message, for real'
                                    }
                    }
        self.pushd = Pushd(self.settings, self.db_manager, templates)
        self.logger = get_logger('test', self.settings)

    def routine(self):
        self.assertTrue(self.pushd.is_alive())
        user_id = self.pushd.users.register('gcm', 'testtoken@!#123')
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


        #unregister user
        self.assertTrue(self.pushd.users.unregister('test@uth.gr'))
    def test_pusd_wrapper(self):
        self.routine()
