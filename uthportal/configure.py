
import json
import os
import sys

from logger import get_logger

CONFIG_FILE = 'config.json'


class Configuration(object):

    default_settings = {
            'database': {
                'host': 'localhost',
                'port': 27017,
                'db_name': 'uthportal'
            },
            'scheduler' : {
                'apscheduler' : { },
                'intervals' : {
                    'CourseTask' : { 'minutes' : 5 },
                    'FoodmenuTask': { 'hours' : 1 },
                    'AnnouncementTask': { 'minutes' : 30 }
                }
            },
            'server' : {
                'host' : '127.0.0.1',
                'port' : 5000,
            },
            'logger': {
                'levels': {
                    'default': 'DEBUG',
                    'mongo': 'DEBUG',
                    'scheduler': 'DEBUG',
                    'apscheduler': 'DEBUG',
                    'uth-portal': 'DEBUG',
                    'uthportal': 'DEBUG'
                }
            },
            'network': {
                'timeout': 10
            },
            'library_path' : 'uthportal/library'
    }

    def __init__(self):
        self.settings = self.default_settings
        self.logger = get_logger(__file__, self.settings)
        self.load_settings()

    def get_settings(self):
        return self.settings

    def set_settings(self, settings):
        """
        Set settings from the supplied ones.
        THis will NOT update the file.
        """
        self.settings = settings

    def load_settings(self):
        self.logger.info('Loading configuration from file...')

        try:
            with open(CONFIG_FILE, 'r') as json_file:
                self.settings = json.load(json_file, encoding = 'utf-8')

        except IOError as e:
            self.logger.warn(
                    "Config file not found! (I/O error({0}): {1}). \
                            Using defualt settings".format(e.errno, e.strerror))
            self.save_settings()

        except:
            self.logger.error("Unexpected error:", sys.exc_info()[0])


        if 'logd_dir' in self.settings:
            log_dir = self.settings['log_dir']
            log_dir = os.path.abspath(log_dir) #convert to absolute path
            if os.path.isdir(log_dir):
                self.setting['log_dir'] = log_dir
                return

        self.settings['log_dir'] = '{0}/logs'.format(os.getcwd())

    def save_settings(self):
        self.logger.info('Saving configuration...')

        try:
            with open(CONFIG_FILE, 'w') as json_file:
                json.dump(self.settings, json_file, sort_keys = True,
                            indent = 4, separators=(',', ': '))

        except IOError as e:
            self.logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
        except:
            self.logger.error("Unexpected error:", sys.exc_info()[0])

