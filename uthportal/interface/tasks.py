from abc import ABCMeta, abstractmethod

class BaseTask(object):
    __metaclass__ = ABCMeta

    def __init__ (self, database_manager, **kwargs):
        self.args = kwargs
        self.database_manager = database_manager

    @abstractmethod
    def fetch(self, *args, **kwargs):
        """Fetch a remote document to be parsed later"""
        return

    def update(self, *args, **kwargs):
        """ Performs the update routine """
        return

    def save(self, *args, **kwargs):
        #TODO: implement
        """Save result dictionary in database"""
        return

    def load(self, *args, **kwargs):
        #TODO: implement
        """Load old dictionary from database"""
        return

    def __call__(self, *args, **kwargs):
        """This is the method called from the Scheduler when this object is
        next in queue"""

        update(*args, **kwargs)


class CourseTask(BaseTask):

    def __init__():
        pass

