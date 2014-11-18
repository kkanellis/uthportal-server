
import logging
from abc import ABCMeta, abstractmethod

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)

class IDatabaseManager(object):
    __metaclass__ = ABCMeta

    def __init__ (self, **kargs):
        """ info: dictionary of arguments

        Neccessary keys are: host, port & db_name .
        TODO: Maybe use named arguments or get with default values?
        """
        self.info = kargs

    @abstractmethod
    def connect(self, *args, **kargs):
        """ Connect to database. Returns boolean if it was successfull. """
        return

    @abstractmethod
    def disconnect(self):
        """ Disconnect from databse, closing all active connections/queries. """
        return

    @abstractmethod
    def insert_document(self, collection, document, **kargs):
        """ Inserts an entry/document to a table/collection. """
        return

    @abstractmethod
    def remove_document(self, collection, document, **kargs):
        """ Deletes an entry/document from a table/collection. """
        return

    @abstractmethod
    def find_document(self, collection, query, **kargs):
        """ Finds and returns the entry/document from a table/collection. """
        return

    @abstractmethod
    def update_document(self, collection, query, document, **kargs):
        """ Updates an existing document with new data """
        return


class MongoDatabaseManager(IDatabaseManager):

    def __init__(self, **kargs):
        super(MongoDatabaseManager, self).__init__(**kargs)

    def connect(self, *args, **kargs):
        self.client = None

        try:
            self.client = MongoClient(
                    host=self.info['host'],
                    port=self.info['port'],
                    *args, **kargs)

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

    def insert_document(self, collection, document, **kargs):
        pass

    def remove_document(self, collection, document, **kargs):
        pass

    def find_document(self, collection, query, **kargs):
        pass

    def update_document(self, collection, query, document, **kargs):
        pass

