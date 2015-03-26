from uthportal.tasks.base import BaseTask

class AnnouncementTask(BaseTask):
    def __init__(self, database_manager):
        super(AnnouncementTask, self).__init__(database_manager)

    @abstractmethod
    def parse(self, document):
        """Parse the fetced document"""
        return

    @abstractmethod
    def update(self):
        """Parse the fetced document"""
        return


