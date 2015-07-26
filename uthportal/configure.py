
import json
import os
import stat
import sys
from inspect import stack

from uthportal.logger import get_logger

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
                'max_size': 10000000,
                'logs_backup_count': 3,
                'levels': {
                    'default': 'WARN',
                    'mongo': 'WARN',
                    'scheduler': 'WARN',
                    'apscheduler': 'WARN',
                    'uth-portal': 'WARN',
                    'uthportal': 'WARN'
                }
            },
            'network': {
                'timeout': 10
            },
            'library_path': 'uthportal/library',
            'tmp_path': 'uthportal/tmp'
    }

    def __init__(self):
        self.default_settings['log_dir'] = os.path.dirname(os.path.abspath(sys.argv[0])) + '/logs'
        self.settings = self.default_settings
        self.logger = get_logger('init', self.settings)
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
            self._fix_permissions()

        except IOError as e:
            self.logger.warn(
                    "Cannot load config file [{0}]! (Reason: {1}). \
                    Using default settings".format(CONFIG_FILE, e.strerror))
            self.save_settings()

        except:
            self.logger.error("Unexpected error:", sys.exc_info()[0])
            sys.exit(1)


        if 'log_dir' in self.settings:
            log_dir = self.settings['log_dir']
            log_dir = os.path.abspath(log_dir) #convert to absolute path
            self.settings['log_dir'] = log_dir
        else:
            self.logger.warn('No log_dir specified. Using defualt')
            self.settings['log_dir'] = self.default_settings['log_dir']

        #Update our logger based on loaded settings
        self.logger = get_logger('configure', self.settings)
        self.logger.info('Loaded new settings')


    def save_settings(self):
        self.logger.info('Saving configuration...')

        try:
            with open(CONFIG_FILE, 'w') as json_file:
                json.dump(self.settings, json_file, sort_keys = True,
                            indent = 4, separators=(',', ': '))
                self._fix_permissions()

        except IOError as e:
            self.logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
        except:
            self.logger.error("Unexpected error:", sys.exc_info()[0])

    def _fix_permissions(self):
        st = os.stat(CONFIG_FILE)
        if st.st_mode & 0xFFF != 0600 :
            self.logger.info("Fixing permissions...")
            os.chmod(CONFIG_FILE, 0600)
