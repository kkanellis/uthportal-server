#!/usr/bin/env python

import os

from uthportal.configure import settings
from uthportal.logger import get_logger, logging_level
from uthportal.database.mongo import MongoDatabaseManager
from uthportal.scheduler import Scheduler

from pkgutil import walk_packages, iter_modules
from importlib import import_module
from inspect import getmembers, isclass

class UthPortal(object):
    def __init__(self, settings):
        self.logger = get_logger(__name__, logging_level.DEBUG)
        self.settings = settings

        if not ('scheduler' in self.settings and 'database' in self.settings):
            self.logger.error('Missing keys from settings [database, scheduler]')
            return

        self.db_manager = MongoDatabaseManager(**self.settings['database'])
        self.db_manager.connect()

        self.scheduler = None

    def load_tasks(self):
        full_libary_path = os.path.dirname(os.path.abspath(__file__)) + '/' + self.settings['library_path']
        self.logger.info('Modules will be loaded from "%s"' % full_libary_path)

        tasks = {}
        for loader, module, is_pkg in walk_packages([ full_libary_path], onerror = self.import_error):
            #load next package
            current_module = loader.find_module(module).load_module(module)

            if (not is_pkg) :
                instance = None
                class_name = None
                #list all classes
                for name, obj in getmembers(current_module):
                    # class name must be contained in module name e.g.
                    # module name: inf.courses.ce121
                    # class name: ce121
                    # this is to avoid importing interface/base classes
                    if isclass(obj) and (name in current_module.__name__):
                        self.logger.info('Importing: %s object: %s' %(name, obj))
                        class_name = name
                        instance = obj(current_module.__name__, 10, self.db_manager)

                modules = module.split('.')
                current_task = tasks
                for task in modules:
                    if task not in current_task:
                        if task ==  class_name:
                            current_task[task] = instance
                        else:
                            current_task[task] = {}
                    current_task = current_task[task]

        self.tasks = tasks

    def import_error(self, name):
        self.logger.error("Error importing module %s" % name)
        error_type, value, traceback = sys.exc_info()
        self.logger.error(traceback)

    def start(self):
        self._start_scheduler()

    def stop(self):
        pass

    def restart(self):
        self.stop_server()
        self.start_server()

    def _start_server(self):
        pass

    def _stop_server(self):
        pass

    def _start_scheduler(self):
        if self.scheduler:
            self.logger.warning('Scheduler already running...')
            return

        self.logger.debug('Starting the scheduler')

        self.scheduler = Scheduler(
                self.tasks,
                self.settings['scheduler']['intervals'])

        self.scheduler.init(**self.settings['scheduler']['apscheduler'])
        self.scheduler.start()

        self.logger.debug('Scheduler started successfully!')

    def _stop_scheduler(self):
        pass

    def load_settings(self):
        pass

    def save_settings(self):
        pass


import signal
import sys
from time import sleep

uth_portal = None

def signal_handler(signal, frame):
    uth_portal.logger.warn('User interrupt! Exiting....')

    uth_portal.save_settings()
    uth_portal.db_manager.disconnect()
    sys.exit(0)

def main():
    #Handle SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    global uth_portal
    uth_portal = UthPortal(settings)
    uth_portal.load_tasks()
    uth_portal.start()

    while True:
        sleep(2)

if __name__ == '__main__' :
    main()

