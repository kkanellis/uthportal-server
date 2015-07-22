
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

    def insert_document(self, collection, document, **kwargs):
        if collection not in self.db:
            self.db[collection] = [ ]

        self.db[collection].append(document)
        return True

    def remove_document(self, collection, query, multi=False, **kwargs):
        if collection not in self.db:
            return False

        for (index, document) in enumerate(self.db[collection]):
            if all( item in document and query[item] == document[item]
                    for item in query ):
                del self.db[collection][index]

                if not multi:
                    break

        return True

    def find_document(self, collection, query, **kwargs):
        if collection not in self.db:
            return None

        for document in self.db[collection]:
            if all( item in document and query[item] == document[item]
                    for item in query ):
                return document

        return None

    def find_documents(self, collection, query, **kwargs):
        if collection not in self.db:
            return None

        documents = [ ]
        for document in self.db[collection]:
            if all( item in document and query[item] == document[item]
                    for item in query ):
                documents.append(document)

        return documents

    def update_document(self, collection, query, new_document, multi=False, upsert=False, **kwargs):
        if collection not in self.db:
            # If upsert=True then we insert the document
            if upsert:
                return self.insert_document(collection, new_document)

            return None

        found = False
        for (index, document) in enumerate(self.db[collection]):
            if all( item in document and query[item] == document[item]
                    for item in query ):
                self.db[collection][index] = new_document

                found = True
                if not multi:
                    break

        if upsert and not found:
            return self.insert_document(collection, new_document)

        return True

