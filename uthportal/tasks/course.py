from uthportal.tasks.base import BaseTask

class CourseTask(BaseTask):
    task_type = 'CourseTask'

    def __init__(self, path, timeout, database_manager):
        super(CourseTask, self).__init__(path, timeout, database_manager)

        self.update_fields =[ 'announcements.site', 'announcements.eclass' ]
        self.db_query = { 'code' : self.id }
        self.document = self.load()

    def update(self):
        new_document_fields = {
                'announcements.site': self.__check_site(),
                'announcements.eclass': self.__check_eclass()
        }

        super(CourseTask, self).update(new_fields=new_document_fields)

    def __check_site(self):
        link = self.document['announcements']['link_site']
        if not link:
            return None

        html = self.fetch(link)
        if not html:
            return None

        bsoup = self.__getsoup(html)
        if not bsoup:
            return None

        return self.parse_site(bsoup)

    def parse_site(self, bsoup):
        """Parse the fetced document"""
        return None

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

