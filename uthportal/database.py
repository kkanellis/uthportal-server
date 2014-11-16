import logging
from abc import ABCMeta, abstractmethod

from pymongo import MongoClient

logger = logging.getLogger(__name__)

class IDatabaseManager(object):
    __metaclass__ = ABCMeta

    def __init__ (self, **kargs):
        """ info: dictionary of arguments

        Neccessary keys are: host, port & db_name .
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

    def __init(self, **kargs):
        super(MongoDatabaseManager, self).__init__(self, **kargs)

    def connect(self, *args, **kargs):
        try:
            self.client = MongoClient(
                    host=self.info['host'],
                    port=self.info['port'],
                    *args, **kargs)
        except ConnectionFailure:
            logger.error('Cannot connect to database (%s, %s)' % (self.info['host'], self.info['port']))
        except KeyError:
            logger.error('Key not found in info! Host=%s, Port=%s' % (self.info['host'], self.info['port']))
        except TypeError:
            logger.error('Maybe port is NOT (int)? type(port)=%s' % str(type(port)) )
        except Exception as ex:
            logger.error(ex.message)

        # Perform self-check
        if not self.client.alive():
            logger.error('MongoDB client is NOT alive! (%s, %s)' % (self.info['host'], self.info['port']))
        else:
            logger.debug('Connected to MongoDB successfully!')

        return self.client.alive()

    def disconnect(self):
        """ No need to close connections. This is handled by pymongo! """
        self.client.disconnect()

    def insert_document(self, collection, document, **kargs):
        pass

    def remove_document(self, collection, document, **kargs):
        pass

    def find_document(self, collection, query, **kargs):
        pass

    def update_document(self, collection, query, document, **kargs):
        pass

