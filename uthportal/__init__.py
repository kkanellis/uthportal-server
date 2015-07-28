from os.path import dirname, abspath
from pkgutil import walk_packages, iter_modules
from inspect import getmembers, isclass

from uthportal.configure import Configuration
from uthportal.logger import get_logger
from uthportal.database.mongo import MongoDatabaseManager
from uthportal.scheduler import Scheduler
from uthportal.server import Server

class UthPortal(object):

    def __init__(self):
        self.configuration = Configuration()
        self.settings = self.configuration.get_settings()
        self.logger = get_logger('uthportal', self.settings)

       #TODO: Do this check in configuration manager
        if 'scheduler' not in self.settings and 'database' not in self.settings:
            self.logger.error('Missing keys from settings [database, scheduler]')
            return

        self.db_manager = MongoDatabaseManager(self.settings)
        self.db_manager.connect()

        self.load_tasks()

        self.server = Server(self.db_manager, self.settings)
        self.scheduler = Scheduler(
                self.tasks,
                self.settings)


    def load_tasks(self):
        self.logger.info("Loading modules...")
        current_path =  dirname(abspath(__file__))
        full_libary_path = current_path + '/' + self.settings['library_path']
        self.logger.debug('Modules will be loaded from "%s"' % full_libary_path)

        tasks = {}
        tasks_num = 0
        for loader, module, is_pkg in walk_packages(
                [full_libary_path],
                onerror = self._import_error):
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
                        self.logger.debug('Importing: %s object: %s' % (name, obj))
                        tasks_num += 1
                        class_name = name
                        instance = obj(current_module.__name__,
                                        self.settings,
                                        self.db_manager)

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
        self.logger.info('Loaded %s tasks' % tasks_num)

    def _import_error(self, name):
        self.logger.error("Error importing module %s" % name)
        error_type, value, traceback = sys.exc_info()
        self.logger.error(traceback)

    def start(self):
        self._start_scheduler()
        self._start_server()

    def stop(self):
        self.db_manager.disconnect()
        self._stop_server()
        self._save_settings()

    def restart(self):
        self.stop_server()
        self.start_server()

    def _start_server(self):
        self.db_manager.connect()
        self.server.start()

    def _stop_server(self):
        if self.server.is_running :
            self.server.stop()

    def _start_scheduler(self):
        self.logger.debug('Starting the scheduler')

        self.scheduler.init(**self.settings['scheduler']['apscheduler'])
        self.scheduler.start()

        self.logger.debug('Scheduler started successfully!')

    def _force_update(self, job_id = None):
        self.scheduler.force_update(job_id)

    def _stop_scheduler(self):
        pass

    def _load_settings(self):
        self.configuration.load_settings()
        self.settings = self.configuration.get_settings()

    def _save_settings(self):
        self.configuration.set_settings(self.settings)
        self.configuration.save_settings()


INFO = {
    "version": "0.7A",
    "developers": "kkanelis, GeorgeTG",
    "description": """
    UTHPortal is a web-application which is targeted to students
    currently attending University of Thessaly. It's main goal is to provide
    easy and direct access to the necessary information and services, which
    are otherwise scattered around different sites/locations.
    """
}
