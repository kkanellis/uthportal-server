from __future__ import absolute_import

import unittest
import os

from uthportal.users import UserManager
from uthportal.configure import Configuration
from uthportal.logger import get_logger
from uthportal.database.memory import MemoryDatabaseManager

class TestUsersManager(unittest.TestCase):
    def setUp(self):
        self.settings = Configuration().get_settings()
        self.settings['logger']['levels']['notifier'] = 'DEBUG'
        self.db_manager = MemoryDatabaseManager()

        templates = {'very_real_event': {
                                    'title' : 'test',
                                    'msg' : 'this is a message, for real'
                                    }
                    }
        self.user_manager = UserManager(self.settings, self.db_manager)
        self.logger = get_logger('test_users_manager', self.settings)

    def routine(self):
        self.logger.info('Creating user test@uth.gr')
        response = self.user_manager.register_new_user('test@uth.gr')
        self.assertEqual(response[0], 400) #sendgrid must answer with wrong password

        self.logger.info('Searching in database for this new user')
        self.assertTrue('test@uth.gr' in self.user_manager.users.pending)

        self.logger.info('Retrieve user')
        user = self.user_manager.users.pending['test@uth.gr']
        #if this fails, KeyError is thrown
        self.logger.info('user object returned: %s' % str(user))
        self.logger.info('user info: %s' % str(user.info))

        self.logger.info('trying to activate this user')
        self.assertTrue(user.activate(user.info['token']))

        self.logger.info('Searching for this user in active users')
        self.assertTrue('test@uth.gr' in self.user_manager.users.active)

        self.logger.info('trying to retrive user from active users')
        user = self.user_manager.users.active['test@uth.gr']
        #if this fails, KeyError is thrown
        self.logger.info('user object returned: %s' % str(user))
        self.logger.info('user info: %s' % str(user.info))

        self.logger.info('trying to authenticate user')
        self.assertTrue(user.authenticate(user.info['auth_id']))

    def test_usersmanager(self):
        self.routine()
