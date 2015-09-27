from __future__ import absolute_import

import unittest
import os

from uthportal.users import UserManager, NetworkError
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
        try:
            response = self.user_manager.register_new_user('test@uth.gr')
        except NetworkError as error:
            self.assertEqual(error.code, 400)

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

        self.logger.info('deleting user')
        del self.user_manager.users.active['test@uth.gr']
        #if this fails, KeyError is thrown
        self.assertFalse('test@uth.gr' in self.user_manager.users.active)

        #special cases
        self.logger.info('try to get non-existant users')
        self.assertRaises(KeyError, lambda: self.user_manager.users.active['a@a.fail'])
        self.assertRaises(KeyError, lambda: self.user_manager.users.pending['a@a.fail'])

        #
        self.logger.info('Creating user special@uth.gr')

        try:
            response = self.user_manager.register_new_user('special@uth.gr')
        except NetworkError as error:
            self.assertEqual(error.code, 400)

        user = self.user_manager.users.pending['special@uth.gr']
        self.assertFalse(user.activate("asdasd"))
        #TODO: add more


    def test_usersmanager(self):
        self.routine()
