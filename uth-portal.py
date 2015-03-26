#!/usr/bin/env python

from os.path import dirname, abspath
from pkgutil import walk_packages, iter_modules
from importlib import import_module
from inspect import getmembers, isclass

from uthportal.configure import settings
from uthportal.logger import get_logger, logging_level
from uthportal.database.mongo import MongoDatabaseManager
from uthportal.scheduler import Scheduler
from uthportal.server import Server

class UthPortal(object):
    def __init__(self, settings):
        self.logger = get_logger(__file__, logging_level.DEBUG)
        self.settings = settings

        if 'scheduler' not in self.settings and 'database' not in self.settings:
            self.logger.error('Missing keys from settings [database, scheduler]')
            return

        self.db_manager = MongoDatabaseManager(**self.settings['database'])
        self.db_manager.connect()

        self.load_tasks()

        self.server = Server(self.db_manager, self.settings)
        self.scheduler = Scheduler(
                self.tasks,
                self.settings['scheduler']['intervals'])


    def load_tasks(self):
        current_path =  dirname(abspath(__file__))
        full_libary_path = current_path + '/' + self.settings['library_path']
        self.logger.info('Modules will be loaded from "%s"' % full_libary_path)

        tasks = {}
        for loader, module, is_pkg in walk_packages(
                [full_libary_path],
                onerror = self.import_error):
            #Load next package
            current_module = loader.find_module(module).load_module(module)

            if not is_pkg:
                instance = None
                class_name = None
                #list all classes
                for name, obj in getmembers(current_module):
                    # class name must be contained in module name e.g.
                    # module name: inf.courses.ce121
                    # class name: ce121
                    # this is to avoid importing interface/base classes
                    if isclass(obj) and (name in current_module.__name__):
                        self.logger.info('Importing: %s object: %s' % (name, obj))
                        class_name = name
                        instance = obj(current_module.__name__,
                                        current_path + '/' + name,
                                        10, self.db_manager)

                modules = module.split('.')

                current_task = tasks
                for task in modules:
                    if task not in current_task:
                        if task == class_name:
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
        self._start_schedulerr()
        self._start_server()

    def stop(self):
        self.db_manager.disconnect()
        self._stop_server()
        self.save_settings()

    def restart(self):
        self.stop_server()
        self.start_server()

    def _start_server(self):
        self.server.start()

    def _stop_server(self):
        if self.server.is_running :
            self.server.stop()

    def _start_schedulerr(self):
        self.logger.debug('Starting the scheduler')

        self.scheduler.init(**self.settings['scheduler']['apscheduler'])
        self.scheduler.start()

        self.logger.debug('Scheduler started successfully!')

    def _force_update(self, job_id = None):
        self.scheduler.force_update(job_id)

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

    uth_portal.stop()
    sys.exit(0)

def main():
    #Handle SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    global uth_portal
    uth_portal = UthPortal(settings)
    uth_portal.start()

    uth_portal._force_update()

    while True:
        sleep(2)

if __name__ == '__main__' :
    main()

