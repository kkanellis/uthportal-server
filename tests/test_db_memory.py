from __future__ import absolute_import

import unittest
from uthportal.database.memory import MemoryDatabaseManager
from tests.base_db import TestDatabase

class TestMemoryManager(TestDatabase):

    def setUp(self):
        super(TestMemoryManager, self).setUp()
        self.manager = MemoryDatabaseManager()

    def test_db_memory(self):
        self.routine()

