from abc import ABCMeta, abstractmethod

class IDatabaseManager(object):
    __metaclass__ = ABCMeta

    def __init__ (self, **kwargs):
        pass

    @abstractmethod
    def connect(self, *args, **kwargs):
        """ Connect to database. Returns boolean if it was successfull. """
        return

    @abstractmethod
    def disconnect(self):
        """ Disconnect from databse, closing all active connections/queries. """
        return

    @abstractmethod
    def insert_document(self, collection, document, **kwargs):
        """ Inserts an entry/document to a table/collection. """
        return

    @abstractmethod
    def remove_document(self, collection, query, **kwargs):
        """ Deletes an entry/document from a table/collection. """
        return

    @abstractmethod
    def find_document(self, collection, query, **kwargs):
        """ Finds and returns the entry/document from a table/collection. """
        return

    @abstractmethod
    def find_documents(self, collection, query, **kwargs):
        """ Finds and returns all entries/documents from a table/collection. """
        return

    @abstractmethod
    def update_document(self, collection, query, document, **kwargs):
        """ Updates an existing document with new data """
        return

