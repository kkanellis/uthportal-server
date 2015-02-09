
import logging
from interface.database import IDatabaseManager

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

logger = logging.getLogger(__name__)

class MongoDatabaseManager(IDatabaseManager):

    def __init__(self, **kwargs):
        super(MongoDatabaseManager, self).__init__(**kwargs)


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


    def disconnect(self):
        """ No need to close connections. This is handled by pymongo! """
        if not self.client:
            logger.warning('Trying to disconnect from a non-connected mongodb client')
            return

        self.client.disconnect()


    def insert_document(self, collection, document, **kwargs):
        if not self.client:
            logger.error('No active DB connection! Cannot perform an insertion')
            return

        try:
            self.db[collection].insert(document, **kwargs)
        except OperationFailure:
            logger.error('OperationFailure: Cannot insert a document into "%s"' % collection)
            return False

        return True


    def remove_document(self, collection, query, **kwargs):
        if not self.client:
            logger.error('No active DB connection! Cannot perform a deletion')
            return

        try:
            self.db[collection].remove(query, **kwargs)
        except OperationFailure:
            logger.error('OperationFailure: Cannot remove a document into "%s"' % collection)
            return False

        return True


    def find_document(self, collection, query, **kwargs):
        if not self.client:
            logger.error('No active DB connection! Cannot perform a search')
            return

        # Since we are interested in one document, find_one is used.

        try:
            document = self.db[collection].find_one(query, **kwargs)
        except OperationFailure:
            logger.error('OperationFailure: Cannot find a document into "%s"' % collection)
            return None

        return document


    def update_document(self, collection, query, document, **kwargs):
        if not self.client:
            logger.error('No active DB connection! Cannot perform a deletion')
            return

        try:
            self.db[collection].update(query, document, **kwargs)
        except OperationFailure:
            logger.error('OperationFailure: Cannot remove a document into "%s"' % collection)
            return False
        except TypeError:
            logger.error('TypeError: Check document(dict) & upsert(bool)')
            return False

        return True

