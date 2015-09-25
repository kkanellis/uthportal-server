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
        self.assertTrue(self.pushd_wrapper.)

    def test_pusd_wrapper(self):
        self.routine()
