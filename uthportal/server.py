import flask
from json import JSONEncoder

from multiprocessing import Process

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from operator import itemgetter

from logger import get_logger

HTTPCODE_NOT_FOUND = 404
HTTPCODE_NOT_IMPLEMENTED = 501

DEFAULT_HIDDEN_FIELDS = [ '_id', 'auth_type' ]
query_type = {
        'courses': 'code',
        'announce': 'type'
}

app =  flask.Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.errorhandler(HTTPCODE_NOT_FOUND)
def page_not_found(error):
    return json_error(HTTPCODE_NOT_FOUND,'Page not Found')

@app.errorhandler(HTTPCODE_NOT_IMPLEMENTED)
def not_implemented(error):
    return json_error(HTTPCODE_NOT_IMPLEMENTED,'Not implemented')

def json_error(code, message):
    return flask.jsonify( {'error': {'code': code, 'message': message} } ), code

# Overide class for JSONEncoder
class BSONEncoderEx(JSONEncoder):
    def default(self, obj, **kwargs):
        from bson.objectid import ObjectId
        from datetime import datetime

        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return JSONEncoder.default(self, obj, **kwargs)

app.json_encoder = BSONEncoderEx

@app.route('/api/v1/info/<path:url>')
def get_info(url):
    url_parts = url.split('/')

    if len(url_parts) <= 1: # Non-valid request
        flask.abort(HTTPCODE_NOT_FOUND)

    document = None
    if url[-1] == '/': # List all children
        url_parts = url_parts[:-1] # Remove last empty entry
        collection = '.'.join(url_parts)

        children = get_children(collection)

        document = None
        if children:
            document = {
                'children' : children,
                'collection': collection
            }

    else:
        collection = '.'.join(url_parts[:-1])

        # Prepare the query
        (key, id) = (url_parts[-2], url_parts[-1])

        if key in query_type:
            query = { query_type[key] : id }
            document = get_document(collection, query)

    if isinstance(document, dict):
        return flask.jsonify( document )
    else:
        flask.abort(HTTPCODE_NOT_FOUND)


def get_document(collection, query, **kwargs):
    """
    Return the first document that matches the query from the given collection
    """

    document = app.config['db_manager'].find_document('server.' + collection, query=query)
    return remove_keys(document, **kwargs)

def get_children(collection, **kwargs):
    """
    Returns all the children that a collection contains
    """
    documents = app.config['db_manager'].find_documents('server.' + collection)

    children = [ ]
    for document in documents:
        children.append( remove_keys(document, **kwargs) )

    return children

def remove_keys(document, keys=None):
    """
    Remove keys from dictionary
    """

    if keys is None:
        keys = DEFAULT_HIDDEN_FIELDS

    for key in keys:
        if key in document:
            del document[key]

    return document

class Server(object):
    """
    An object-oriented wrapper for the flask-server
    """

    def __init__(self, database_manager, settings):
        self.settings = settings
        self.logger = get_logger(__file__, self.settings)
        self.__database_manager = database_manager

        self.__process = None
        self.__is_running = False

        app.config['db_manager'] = database_manager
        app.config['settings'] = settings

    def start(self):
        if self.__is_running:
            self.logger.error("Cannot start. Server is already running!!!")
            return

        self.__is_running = True
        self.__process = Process(target = self.__start_flask)
        self.__process.start()

        self.logger.info("Server started.")

    def stop(self):
        if not self.__is_running:
            self.logger.error("Cannot stop. Server is not running!!!")
            return

        self.__process.terminate()
        self.__is_running = False

        self.logger.info("Server stopped.")

    def is_running(self):
        return self.__is_running

    def __start_flask(self):
        server_settings = self.settings['server']
        app.run(host = server_settings['host'], port = server_settings['port'])

