
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

from uthportal.database.database import IDatabaseManager
from uthportal.logger import get_logger

class MongoDatabaseManager(IDatabaseManager):

    def __init__(self, settings, **kwargs):
        """
        Neccessary keys are: host, port & db_name .
        TODO: Maybe use named arguments or get with default values?
        """
        self.settings = settings
        self.logger = get_logger(__file__, self.settings)

        self.client = None

        self.info = self.settings['database']

        if (not self.info['host'] or
            not self.info['port'] or
            not self.info['db_name']):
                self.logger.error('An argument is missing [host|port|db_name]')

    def _requires_client(function):
        def new_func(self, *args, **kwargs):
            if not self.client:
                self.logger.error('Cannot complete action: [%s], database not connected' % function.__name__)
                return False
            else:
                return function(self, *args, **kwargs)

        return new_func

    def connect(self, *args, **kwargs):
        self.client = None

        try:
            self.client = MongoClient(
                    host=self.info['host'],
                    port=self.info['port'],
                    *args, **kwargs)

            # Store the database
            db_name = self.info['db_name']
            self.db = self.client[db_name]

        except ConnectionFailure:
            self.logger.error('ConnectionFailure: Cannot connect to database (%s, %s)' % (self.info['host'], self.info['port']))
        except KeyError:
            self.logger.error('KeyError: Check arguments host & port arguments')
        except TypeError:
            self.logger.error('TypeError: Maybe port is NOT (int)? type(port)=%s' % str(type(self.info['port'])))
        except Exception as ex:
            self.logger.error(ex.message)

        # Perform self-check
        if not self.client:
            self.logger.error('Connection to MongoDB was unsuccessfull')
            return False

        self.logger.debug('Connected to MongoDB successfully!')
        return True

    @_requires_client
    def disconnect(self):
        """ No need to close connections. This is handled by pymongo! """
        self.client.disconnect()

        return True

    @_requires_client
    def insert_document(self, collection, document, **kwargs):
        try:
            self.db[collection].insert(document, **kwargs)
        except OperationFailure, e:
            self.logger.error('OperationFailure: Cannot insert a document into "%s": %s' % (collection, unicode(e)))
            return False

        return True


    @_requires_client
    def remove_document(self, collection, query, **kwargs):

        try:
            self.db[collection].remove(query, **kwargs)
        except OperationFailure, e:
            self.logger.error('OperationFailure: Cannot remove a document into "%s": %s' % (collection, unicode(e)))
            return False

        return True

    @_requires_client
    def find_document(self, collection, query=None, **kwargs):
        # Since we are interested in one document, find_one is used.
        if query is None:
            query = { }

        document = None
        try:
            document = self.db[collection].find_one(query, **kwargs)
        except OperationFailure, e:
            self.logger.error('OperationFailure: Cannot find a document into "%s": %s' % (collection, unicode(e)))
            return None

        return document


    @_requires_client
    def find_documents(self, collection, query=None, **kwargs):
        if query is None:
            query = { }

        documents = None
        try:
            documents = self.db[collection].find(query, **kwargs)
        except OperationFailure, e:
            self.logger.error('OperationFailure: Cannot find documents into "%s": %s' % (collection, unicode(e)))
            return None

        return documents


    @_requires_client
    def update_document(self, collection, query, document, **kwargs):

        try:
            self.db[collection].update(query, document, **kwargs)
        except OperationFailure, e:
            self.logger.error('OperationFailure: Cannot update a document into "%s": %s' % (collection, unicode(e)))
            return False
        except TypeError, e:
            self.logger.error('TypeError: Check document(dict) & upsert(bool): %s', e)
            return False

        return True

    @_requires_client
    def drop_collection(self, collection, **kwargs):
        try:
            self.db.drop_collection(collection)
        except Exception, e:
            self.logger.error(e)
            return False

        return True


