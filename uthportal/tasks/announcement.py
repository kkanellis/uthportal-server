import requests

from uthportal.tasks.base import BaseTask

class AnnouncementTask(BaseTask):
    def __init__(self, path, timeout, database_manager):
        super(AnnouncementTask, self).__init__(path, timeout, database_manager)

        self.update_fields = [ 'entries' ]
        self.db_query = { 'type' : self.id }

        self.logger.debug('Loading document from database...')

        self.document = self.load()
        if not self.document:
            if hasattr(self, 'document_prototype'):
                self.logger.info('No document found in database. Using prototype')
                self.document = self.document_prototype
                self.save()
            else:
                self.logger.error('No document_prototype is available!')
                return

    def update(self):
        new_document_fields = {
                'entries' : self._check_source()
        }

        # Check any new data exist
        if new_document_fields['entries']:
            super(CourseTask, self).update(new_fields=new_document_fields)
        else:
            self.logger.warning('RSS returned no data')

    def _check_source(self):






    def _make_auth(self, link, payload, session):
        """ Makes an http POST request in order to login where needed """
        try:
            auth_response = session.post(link, verify=False, data=payload)
        except ConnectionError:
            self.logger.warning('%s: Connection error' % link)
            return None
        except Timeout:
            self.logger.warning('%s: Timeout [%d]' % (link, self.timeout))
            return None

        if page.status_code is not (200 or 301):
            self.logger.warning('%s: Returned [%d]' % (link, page.code))
            return None

        return auth_response

    def _get_auth_info(self, type):
        query = { 'type' : type }
        document = self.database_manager.find_document('auth', query)

        if document and '_id' in document:
            del document['_id']
        else:
            self.logger.error('No auth info found for type "%s"' % type)

        return document

