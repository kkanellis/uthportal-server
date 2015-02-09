from abc import ABCMeta, abstractmethod

class BaseTask(object):
    __metaclass__ = ABCMeta

    def __init__(self, database_manager, **kwargs):
        self.database_manager = database_manager

    @abstractmethod
    def fetch(self, *args, **kwargs):
        """Fetch a remote document to be parsed later"""
        return

    def save(self, *args, **kwargs):
        #TODO: implement
        """Save result dictionary in database"""
        return

    def load(self, *args, **kwargs):
        #TODO: implement
        """Load old dictionary from database"""
        return

    @abstractmethod
    def update(self):
        """This function is called from __call__"""
        return

    def __call__(self, *args, **kwargs):
        self.update()


class CourseTask(BaseTask):
    def __init__(self, database_manager):
        super(CourseTask, self).__init__(database_manager)

    def fetch(self, *args, **kwargs):
        #TODO: implement
        """Fetch a remote document to be parsed later"""
        return

    def parse_site(self, *args, **kwargs):
        #TODO: implement
        """Parse the fetced document"""
        return

    def parse_eclass(self, *args, **kwargs):
        #TODO: implement
        """Parse the fetced document"""
        return


    def postprocess_site(self, *args, **kwargs):
        #TODO: implement
        """Process the document before saving"""
        return


    class CourseTask(BaseTask):
        def __init__(self, database_manager):
            super(CourseTask, self).__init__(database_manager)



