from __future__ import absolute_import

import unittest
import os

from uthportal.notifier import PushdWrapper
from uthportal.configure import Configuration
from uthportal.logger import get_logger
from uthportal.database.memory import MemoryDatabaseManager

class TestPushWrapper(unittest.TestCase):
    def setUp(self):
        self.settings = Configuration().get_settings()
        self.settings['log_dir'] = os.path.abspath("test_logs")
        self.settings['logger']['levels']['notifier'] = 'DEBUG'
        self.db_manager = MemoryDatabaseManager()
        self.pushd_wrapper = PushdWrapper(self.settings, self.db_manager)

    def routine(self):
        self.assertTrue(self.pushd_wrapper.is_alive())
        user_id = self.pushd_wrapper.users.register('gcm', 'testtoken@!#123')
        self.assertIsNotNone(user_id)
        #Add user to databse
        self.db_manager.insert_document("users.active",
        {'email' : 'test@uth.gr', 'token': '12345678', 'pushd_id': user_id})
        self.assertTrue(self.pushd_wrapper.users.exists('test@uth.gr'))
        #try to get user with getter
        pushd_user = self.pushd_wrapper.users['test@uth.gr']
        self.assertIsNotNone(pushd_user)

    def test_pusd_wrapper(self):
        self.routine()
