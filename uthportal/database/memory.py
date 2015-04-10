
from database import IDatabaseManager

class MemoryDatabaseManager(IDatabaseManager):
    """ Database manager which stores data in memory (no persistence).
        Used for testing. """

    def __init__(self):
        self.db = { }

    def connect(self):
        return True

    def disconnect(self):
        return True

    def insert_document(self, collection, document):
        if collection not in self.db:
            self.db[collection] = [ ]

        self.db[collection].append(document)
        return True

    def remove_document(self, collection, query, multi=False):
        if collection not in self.db:
            return None

        found = False
        for (index, document) in enumerate(self.db[collection]):
            if all( item in document and query[item] == document[item]
                    for item in query ):
                found = True
                del self.db[collection][index]

                if not multi:
                    break

        return True

    def find_document(self, collection, query):
        if collection not in self.db:
            return None

        for document in self.db[collection]:
            if all( item in document and query[item] == document[item]
                    for item in query ):
                return document

        return None

    def find_documents(self, collection, query):
        if collection not in self.db:
            return None

        documents = [ ]
        for document in self.db[collection]:
            if all( item in document and query[item] == document[item]
                    for item in query ):
                documents.append(document)

        return documents

    def update_document(self, collection, query, new_document, multi=False):
        if collection not in self.db:
            return None

        for (index, document) in enumerate(self.db[collection]):
            if all( item in document and query[item] == document[item]
                    for item in query ):
                self.db[collection][index] = new_document

                if not multi:
                    break

        return True

