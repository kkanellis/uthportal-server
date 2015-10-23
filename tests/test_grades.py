import unittest
from cred import credentials

from uthportal.grades import GradesProvider
from uthportal.configure import Configuration
from uthportal.logger import get_logger
from uthportal.database.memory import MemoryDatabaseManager
class TestGradesProvider(unittest.TestCase):
    def setUp(self):
        self.settings = Configuration().get_settings()
        self.settings['logger']['levels']['grades'] = 'DEBUG'
        self.db_manager = MemoryDatabaseManager()
        self.grades_provider = GradesProvider(self.settings)
        self.logger = get_logger('test_users_manager', self.settings)

    def routine(self):
        self.assertTrue(self.grades_provider._check_vpn())
        self.assertTrue(
            self.grades_provider.login(
                credentials['uname'],
                credentials['passwd']
            )
        )
        self.assertIsNotNone(self.grades_provider.get_grades())
        self.assertTrue(self.grades_provider.logout())

    def test_grades_provider(self):
        self.routine()
