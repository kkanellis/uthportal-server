from uthportal.tasks.base import BaseTask

class AnnouncementTask(BaseTask):
    def __init__(self, database_manager):
        super(AnnouncementTask, self).__init__(database_manager)

    def fetch(self, *args, **kwargs):
        #TODO: implement
        """Fetch a remote document to be parsed later"""
        return

    def parse(self, document):
        """Parse the fetced document"""
        return

