#!/usr/bin/env python

"""
fields:

DatabaseManager, NotifierManager
tasks
settings

server_thread

functions:

__init__: Call function to read configuration files. Call functions to create tree from tasks. Instantiate the databasemanager, notifiermanager, scheduler.

read_settings()

create_task_tree(tasks_dir)

start_server()

stop_server()

restart()
"""

from uthportal.logger import get_logger, logging_level
from uthportal.database import MongoDatabaseManager
from uthportal.scheduler import Scheduler
#from uthportal.server import ....
import logging

from pkgutil import walk_packages, iter_modules
from importlib import import_module
from inspect import getmembers, isclass

from uthportal import library
from uthportal.library import inf

class UthPortal(object):
    def __init__(self):
        import inspect
        name = inspect.stack()[0][1] #get filename

        self.logger = get_logger(name, logging.DEBUG)
        return

    def load_tasks(self, package):
        tasks = {}
        for loader, module, is_pkg in walk_packages(package.__path__, onerror = self.import_error):
            #load next package
            current_module = loader.find_module(module).load_module(module)

            if (not is_pkg) :
                #list all classes
                for name, obj in getmembers(current_module):
                    # class name must be contained in module name e.g.
                    # module name: inf.courses.ce121
                    # class name: ce121
                    # this is to avoid importing interface classes
                    if isclass(obj) and (name in current_module.__name__):
                        self.logger.info('Importing: %s object: %s' %(name, obj))
                        instance = obj(None) #we should be using db_manager here

                modules = module.split('.')
                #TODO: make the tree


    def import_error(self, name):
        print("Error importing module %s" % name)
        error_type, value, traceback = sys.exc_info()
        print(traceback)

    def start_server(self):
        pass

    def stop_server(self):
        pass

    def restart_server(self):
        self.stop_server()
        self.start_server()

    def load_settings(self):
        pass

    def save_settings(self):
        pass


import signal
import sys
from time import sleep

uth_portal = None

def signal_handler(signal, frame):
    uth_portal.logger.warn('User interrupt!')
    uth_portal.save_settings()
    sys.exit(0)

def main():
    #Handle SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    global uth_portal
    uth_portal = UthPortal()

    uth_portal.load_tasks(library)
    while True:
        sleep(2)

if __name__ == '__main__' :
    main()

