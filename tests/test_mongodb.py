from __future__ import absolute_import

import unittest
from uthportal.database.mongo import MongoDatabaseManager
from tests.base_db import TestDatabase

class TestMongoManager(TestDatabase):

    def setUp(self):
        super(TestMongoManager, self).setUp()

        settings = {
                'database': {
                    'host': 'localhost',
                    'port': 27017,
                    'db_name': 'test_db'
                },
                'logger': {
                    'max_size': 10000000,
                    'logs_backup_count': 3,
                    'levels': {
                        'mongo': 'DEBUG'
                    }
                }
        }
        self.manager = MongoDatabaseManager(settings)

    def tearDown(self):
        self.manager.drop_collection('test')

    def test_mongo(self):
        self.routine()

