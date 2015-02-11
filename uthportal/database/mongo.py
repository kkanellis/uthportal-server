import inspect, logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

from uthportal.database.database import IDatabaseManager
from uthportal.logger import get_logger, logging_level

name = inspect.stack()[0][1] #get filename

logger = get_logger(name, logging.DEBUG)

def check_connected(function):
    def new_func(self, *args, **kwargs):
        if not self.client:
            logger.error('Cannot complete action: [%s], database not connected' % func.__name__)
            return False
        else:
            function(self, *args, **kwargs)

    return new_func


class MongoDatabaseManager(IDatabaseManager):

    def __init__(self, **kwargs):
        """
        Neccessary keys are: host, port & db_name .
        TODO: Maybe use named arguments or get with default values?
        """
        self.client = None

        if not all(key in kwargs for key in ('host', 'port', 'db_name')):
            logger.error('Some necessary kwargs (host, port, db_name) are missing')
            return

        self.info = kwargs

    def connect(self, *args, **kwargs):
        self.client = None

        try:
            self.client = MongoClient(
                    host=self.info['host'],
                    port=self.info['port'],
                    *args, **kwargs)

            # Store the database
            self.db = self.client['db_name']

        except ConnectionFailure:
            logger.error('ConnectionFailure: Cannot connect to database (%s, %s)' % (self.info['host'], self.info['port']))
        except KeyError:
            logger.error('KeyError: Check arguments host & port arguments')
        except TypeError:
            logger.error('TypeError: Maybe port is NOT (int)? type(port)=%s' % str(type(self.info['port'])))
        except Exception as ex:
            logger.error(ex.message)

        # Perform self-check
        if not self.client:
            logger.error('Connection to MongoDB was unsuccessfull')
            return False

        logger.debug('Connected to MongoDB successfully!')
        return True

    @check_connected
    def disconnect(self):
        """ No need to close connections. This is handled by pymongo! """
        self.client.disconnect()

    @check_connected
    def insert_document(self, collection, document, **kwargs):
        try:
            self.db[collection].insert(document, **kwargs)
        except OperationFailure:
            logger.error('OperationFailure: Cannot insert a document into "%s"' % collection)
            return False

        return True


    @check_connected
    def remove_document(self, collection, query, **kwargs):

        try:
            self.db[collection].remove(query, **kwargs)
        except OperationFailure:
            logger.error('OperationFailure: Cannot remove a document into "%s"' % collection)
            return False

        return True

    @check_connected
    def find_document(self, collection, query, **kwargs):
        # Since we are interested in one document, find_one is used.

        try:
            document = self.db[collection].find_one(query, **kwargs)
        except OperationFailure:
            logger.error('OperationFailure: Cannot find a document into "%s"' % collection)
            return None

        return document

    @check_connected
    def update_document(self, collection, query, document, **kwargs):

        try:
            self.db[collection].update(query, document, **kwargs)
        except OperationFailure:
            logger.error('OperationFailure: Cannot remove a document into "%s"' % collection)
            return False
        except TypeError:
            logger.error('TypeError: Check document(dict) & upsert(bool)')
            return False

        return True

