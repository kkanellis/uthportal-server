#!/usr/bin/env python2.7

from datetime import datetime, timedelta
from json import JSONEncoder
from operator import itemgetter
import re

import flask
import sendgrid
from bs4 import BeautifulSoup

from uthportal.database.mongo import MongoDatabaseManager
from uthportal.configure import Configuration
from uthportal.logger import get_logger
from uthportal.users import  UserManager, RegistrationError, NetworkError, ActivationError
from uthportal.util import BSONEncoderEx

HTTPCODE_NOT_FOUND = 404
HTTPCODE_BAD_REQUEST = 400
HTTPCODE_TOO_MANY_REQUESTS = 429
HTTPCODE_NOT_IMPLEMENTED = 501
HTTPCODE_SERVICE_UNAVAILABLE = 503

DEFAULT_EXCLUDED_FIELDS = [ '_id', 'auth_type' ]
query_type = {
        'courses': 'code',
        'announce': 'type',
        'food': 'city',
        'inf': 'type'
}

ALLOWED_DOMAINS = ['uth.gr', 'inf.uth.gr']

app =  flask.Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

app.json_encoder = BSONEncoderEx

db_manager = None
settings = None
logger = None
user_manager = None

@app.errorhandler(HTTPCODE_NOT_FOUND)
def page_not_found(error):
    return json_error(HTTPCODE_NOT_FOUND,'Page not Found')

@app.errorhandler(HTTPCODE_NOT_IMPLEMENTED)
def not_implemented(error):
    return json_error(HTTPCODE_NOT_IMPLEMENTED,'Not implemented')

def json_error(code, message):
    return flask.jsonify(
        {'response': {
            'code': code,
            'message': message,
            'type': 'ERROR'
            }
        }), code

def json_ok(message):
    return flask.jsonify(
        {'response': {
            'code': 200,
            'message': message,
            'type': 'OK'
            }
        }), 200

def db_collection(collection):
    return 'server.' + collection

@app.route('/api/v1/users/activate', methods=['GET'])
def activate():
    global db_manager, logger, settings, user_manager

    token = flask.request.args.get('token')
    email = flask.request.args.get('email')
    if token is None or email is None:
        return 'No token or email provided', HTTPCODE_BAD_REQUEST

    logger.info('User trying to activate with email: {0}, and token: {1}'.format(
        email, token)
    )

    if email not in user_manager.users.pending:
        return 'No pending user with this email', HTTPCODE_BAD_REQUEST

    user = user_manager.users.pending[email]
    try:
        user.activate(token)
        logger.info('User activated successfully :%s' % email)
        return 'User activated successfully', 200
    except ActivationError as error:
        return error.message, error.code

@app.route('/api/v1/users/register', methods=['POST'])
def register():
    global db_manager, logger, settings, user_manager

    email = flask.request.args.get('email')
    if email == None:
        return json_error(HTTPCODE_BAD_REQUEST, 'No email address')

    logger.info('User trying to register with email: ' + email)
    match = re.match(r'[^@]+@([^@]+\.[^@]+)', email)

    if match == None:
        return json_error(HTTPCODE_BAD_REQUEST, 'Bad email address')

    #check if this address has a uth domain
    email_domain = match.group(1)
    if not email_domain in ALLOWED_DOMAINS:
        return  json_error(HTTPCODE_BAD_REQUEST, 'Bad email domain: ' + email_domain)

    if not email in user_manager.users.pending:
        try:
            user_manager.register_new_user(email)
            logger.info('User [%s] registered successfuly. Activation mail sent!' % email)
            return json_ok('Activation email sent!')
        except RegistrationError as error:
            return json_error(HTTPCODE_BAD_REQUEST, error.message)
        except NetworkError as error:
            #this means our user is stored in the database, but we can't send
            #activation email
            return json_error(error.code, error.message + "Issue an email resend request later.")
    else:
        return json_error(HTTPCODE_BAD_REQUEST, 'User already registered.')

@app.route('/api/v1/info/<path:url>', methods=['GET'])
def get_info(url):
    url_parts = url.split('/')

    if len(url_parts) <= 1: # Non-valid request
        flask.abort(HTTPCODE_NOT_FOUND)

    exclude_param = flask.request.args.get('exclude')
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

def main():
    global db_manager, settings, logger, app, user_manager

    settings = Configuration().get_settings()
    logger = get_logger('server', settings)

    logger.info('Connecting to database...')
    db_manager = MongoDatabaseManager(settings)
    db_manager.connect()

    user_manager = UserManager(settings, db_manager)

    server_settings = settings['server']
    app.run(host = server_settings['host'], port = server_settings['port'])

if __name__ == '__main__':
    main()
