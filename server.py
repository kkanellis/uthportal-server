#!/usr/bin/env python2.7

import flask
from flask import request
from json import JSONEncoder

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from operator import itemgetter

from uthportal.database.mongo import MongoDatabaseManager
from uthportal.configure import Configuration
from uthportal.logger import get_logger
from uthportal.util import BSONEncoderEx

HTTPCODE_NOT_FOUND = 404
HTTPCODE_NOT_IMPLEMENTED = 501

DEFAULT_EXCLUDED_FIELDS = [ '_id', 'auth_type' ]
query_type = {
        'courses': 'code',
        'announce': 'type',
        'food': 'city',
        'inf': 'type'
}

app =  flask.Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

app.json_encoder = BSONEncoderEx

db_manager = None
settings = None
logger = None

@app.errorhandler(HTTPCODE_NOT_FOUND)
def page_not_found(error):
    return json_error(HTTPCODE_NOT_FOUND,'Page not Found')

@app.errorhandler(HTTPCODE_NOT_IMPLEMENTED)
def not_implemented(error):
    return json_error(HTTPCODE_NOT_IMPLEMENTED,'Not implemented')

def json_error(code, message):
    return flask.jsonify( {'error': {'code': code, 'message': message} } ), code

def db_collection(collection):
    return 'server.' + collection

@app.route('/api/v1/info/<path:url>', methods=['GET'])
def get_info(url):
    url_parts = url.split('/')

    if len(url_parts) <= 1: # Non-valid request
        flask.abort(HTTPCODE_NOT_FOUND)

    exclude_param = request.args.get('exclude')
    exclude_fields = exclude_param.split(',') if exclude_param else [ ]

    document = None
    if url[-1] == '/': # List all children
        url_parts = url_parts[:-1] # Remove last empty entry
        collection = '.'.join(url_parts)

        children = get_children(collection, exclude_fields)

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
            document = get_document(collection, query, exclude_fields)

    if isinstance(document, dict):
        return flask.jsonify( document )
    else:
        flask.abort(HTTPCODE_NOT_FOUND)


def get_document(collection, query, exclude_keys):
    """
    Return the first document that matches the query from the given collection
    """
    document = db_manager.find_document( db_collection(collection), query=query)
    return remove_keys(document, exclude_keys) if document else None

def get_children(collection, exclude_keys):
    """
    Returns all the children that a collection contains
    """
    documents = db_manager.find_documents( db_collection(collection) )
    return [ remove_keys(document, exclude_keys) for document in documents if document ]

def remove_keys(document, keys):
    """
    Remove keys from dictionary
    """
    # Add the default excluded fields
    keys = keys + DEFAULT_EXCLUDED_FIELDS

    for key in keys:
        document.pop(key, None)

    return document


def __start_flask(self):
    server_settings = self.settings['server']


def main():
    global db_manager, settings, logger, app
    settings = Configuration().get_settings()
    logger = get_logger('server', settings)

    logger.info('Connecting to database...')
    db_manager = MongoDatabaseManager(settings)
    db_manager.connect()

    server_settings = settings['server']
    app.run(host = server_settings['host'], port = server_settings['port'])

if __name__ == '__main__':
    main()
