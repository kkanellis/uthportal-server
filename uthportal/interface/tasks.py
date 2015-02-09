from abc import ABCMeta, abstractmethod
import logging
from datetime import datetime

import requests
from requests.exceptions import ConnectionError, Timeout
import feedparser

from uthportal.database import MongoDatabaseManager


logger = logging.getLogger(__name__)

class BaseTask(object):
    __metaclass__ = ABCMeta

    def __init__(self, path, timeout, database_manager, **kwargs):
        self.path = path
        self.timeout = timeout
        self.database_manager = database_manager

        self.id = path.split('.')[-1]
        self.db_collection = path.split('.')[:-1]

    def fetch(self, link):
        """Fetch a remote document to be parsed later"""
        try:
            page = requests.get(link, timeout=self.timeout)
        except ConnectionError:
            logger.warning('[%s] %s: Connection error' % (self.id, link))
            return None
        except Timeout:
            logger.warning('[%s] %s: Timeout [%d]' % (self.id, link, self.timeout))
            return None

        if page.code is not (200 or 301):
            logger.warning('[%s] %s: Returned [%d]' % (self.id, link, page.code))
            return None

        page.encoding = 'utf-8'
        return page.text

    @abstractmethod
    def update(self, *args, **kwargs):
        """This function is called from __call__"""

        old = kwargs['old']
        new = kwargs['new']
        if not old or not new:
            return

        differ = False
        for key in new: # This will be changed. Too swag code
            if new[key] and key in old and old[key] and new[key] != old[key]:
                differ = True
                break

        if differ:
            self.archive()
            self.update_document(new)
            self.update_server()
            self.notify()
        else:
            self.db_document['last_updated'] = datetime.now()

        self.save()

    def update_document(self, entries):
        new_document = self.db_document

        keys_exist = True
        for field in self.fields:
            if not field in entries:
                keys_exist = False
                break

            self.__set_document_field(self, new_document, field, entry[field])

        if keys_exist:
            new_document['first_updated'] = new_document['last_updated'] = datetime.now()
            self.db_document = new_document
        else:
            pass


    def notify(self):
        pass

    def save(self, *args, **kwargs):
        """Save result dictionary in database"""
        if not self.database_manager.update_document(self.db_collection, self.db_query, self.db_document, *args, **kwargs):
            logger.warning('Could not save document "%s"' % self.path)

    def archive(self, *args, **kwargs):
        """ Save the current document into the history collection """
        if not self.database_manager.insert_document('history.%s' % self.db_collection, self.db_document, *args, **kwargs):
            logger.warning('Could not archive document "%s"' % self.path)

    def load(self, *args, **kwargs):
        """Load old dictionary from database"""
        return self.database_manager.find_document(self.db_collection, self.db_query, *args, **kwargs)

    def __call__(self):
        """This is the method called from the Scheduler when this object is
        next in queue"""

        self.update()


class CourseTask(BaseTask):
    def __init__(self, path, timeout, database_manager):
        super(CourseTask, self).__init__(path, timeout, database_manager)

        self.fields = { 'announcements.site', 'announcements.eclass' }
        self.db_query = { 'code' : self.id }
        self.db_document = self.load()

    def update(self):
        old = {
                'site': self.db_document['announcements']['site'],
                'eclass': self.db_document['announcements']['eclass']
        }
        new = {
                'site': self.__check_site(),
                'eclass': self.__check_eclass()
        }

        super(CourseTask, self).update(old=old, new=new)

    def __check_site(self):
        link = self.db_document['announcements']['link_site']
        if not link:
            return None

        html = self.fetch(link)
        if not html:
            return None

        bsoup = self.__getsoup(html)
        if not bsoup:
            return None

        return self.parse_site(bsoup)

    @abstractmethod
    def parse_site(self, bsoup):
        """Parse the fetced document"""
        return

    def parse_eclass(self):
        """Parse the fetced document"""
        try:
            rss = feedparser.parse(html)
        except Exception, e:
            logger.error('[%s] %s' % (self.id, e))
            return None

        # Datetime format
        # dt_format = '%a, %d %b %Y %H:%M:%S %z'
        entries = None
        try:
            entries = [{
                        'title': entry.title,
                        'html': entry.description,
                        'plaintext': __get_soup(entry.description).text,
                        'link': entry.link,
                        'date': datetime.fromtimestamp(mktime(entry.published_parsed)),
                        'has_time': True
                        }
                        for entry in rss.entries ]
        except Exception, e:
            logger.error('[%s] %s' %  (self.id, e))

        return entries

    def postprocess_site(self, *args, **kwargs):
        #TODO: implement
        """Process the document before saving"""
        pass

    def __getsoup(html):
        """ Returns the BeautifulSoup object from the html """
        bsoup = None
        try:
            bsoup = BeautifulSoup(html)
        except Exception, e:
            logger.error('[%s] Error while parsing html: %s' % (self.id, e))

        return bsoup


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

class FoodmenuTask(BaseTask):
    def __init__(self, database_manager):
        super(FoodmenuTask, self).__init__(database_manager)

    def fetch(self, *args, **kwargs):
        #TODO: implement
        """Fetch a remote document to be parsed later"""
        return

    def parse(self, document):
        """Parse the fetced document"""
        return


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    a = CourseTask('inf.courses.ce120', 5, MongoDatabaseManager())

