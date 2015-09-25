from __future__ import absolute_import

import unittest

from uthportal.database.mongo import MongoDatabaseManager
from uthportal.configure import Configuration
from tests.base_db import TestDatabase

class TestMongoManager(TestDatabase):

    def setUp(self):
        super(TestMongoManager, self).setUp()

        self.settings = Configuration().get_settings()
        self.settings['database'] = {
                    'host': 'localhost',
                    'port': 27017,
                    'db_name': 'test_db'
                }
        self.settings['logger'] = {
                    'max_size': 10000000,
                    'logs_backup_count': 3,
                    'levels': {
                        'mongo': 'DEBUG'
                    }
                }

        self.manager = MongoDatabaseManager(self.settings)

    def tearDown(self):
        self.manager.drop_collection('test')

    def test_mongo(self):
        self.routine()
