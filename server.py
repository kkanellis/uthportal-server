#!/usr/bin/env python2.7

from datetime import datetime, timedelta
from json import JSONEncoder
from operator import itemgetter
import re

import flask
import sendgrid
from flask import request
from bs4 import BeautifulSoup

from uthportal.database.mongo import MongoDatabaseManager
from uthportal.configure import Configuration
from uthportal.logger import get_logger
from uthportal.users import  UserControl
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

app =  flask.Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

app.json_encoder = BSONEncoderEx

db_manager = None
settings = None
logger = None
user_control = None

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

@app.route('/api/v1/register', methods=['POST'])
def register():
    global db_manager, logger, settings
    email = request.args.get('email')
    if email == None:
        return json_error(HTTPCODE_BAD_REQUEST, 'No email address')
    logger.info('User trying to register with email: ' + email)
    match = re.match(r'[^@]+@([^@]+\.[^@]+)', email)

    if match == None:
        return json_error(HTTPCODE_BAD_REQUEST, 'Bad email address')

    email_domain = match.group(1)
    if not (email_domain == 'uth.gr' or email_domain == 'inf.uth.gr'):
        return  json_error(HTTPCODE_BAD_REQUEST, 'Bad email domain: ' + email_domain)

    user = db_manager.find_document('users.active', {'email': email})
    if user == None:
       #no active user found
        user = db_manager.find_document('users.pending', {'email': email})
        if user == None:
            logger.debug('[%s] no pending user found with this email' % email)
            #no pending user found. We have a valid application
            (userid, token) = user_control.generate_and_check()
            logger.debug('[{0}] -> generated userid:{1}, token {2}'.format(email, userid, token))
            #Send activation email
            (status, msg) = user_control.send_activation_email(email, userid, token)
            logger.debug('SendGrid response: [{0}] -> {1}'.format(status, msg))

            if int(status) < 400 :
                #email sent, register this user as pending
                db_manager.insert_document('users.pending',
                { 'email' : email, 'userid': userid, 'token': token, 'tries': 1 })
                return flask.jsonify( {'message' : "Confirmation email with activation link sent."} )
            else:
                #email service returned an error
                json_error(HTTPCODE_SERVICE_UNAVAILABLE, 'Email service unavailable')
        else:
            #there is already a pending user
            tries = user['tries']
            logger.info('[{0}][PENDING] resend requested, tries{1}'.format(email, tries))
            if (tries < 5):
                try:
                    userid = user['userid']
                    token = user['token']
                except KeyError as key_error:
                    logger.error('KeyError: %s' % key_error)
                    json_error(HTTPCODE_SERVICE_UNAVAILABLE, 'Service unavailable')
                (status, msg) = user_control.send_activation_email(email, userid, token)
                logger.debug('SendGrid response: [{0}] -> {1}'.format(status, msg))
                user['tries'] = tries + 1
                return flask.jsonify( {'message' : "Confirmation email with activation link sent."} )
            else:
                return json_error(HTTPCODE_TOO_MANY_REQUESTS, 'Max code resend tries exceeded.')
    else:
        #user is active
        return  json_error(HTTPCODE_BAD_REQUEST, 'An active user with this email already exists!')

    return json_error(HTTPCODE_BAD_REQUEST, 'Failed')

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
    global db_manager, settings, logger, app, user_control
    settings = Configuration().get_settings()
    logger = get_logger('server', settings)

    logger.info('Connecting to database...')
    db_manager = MongoDatabaseManager(settings)
    db_manager.connect()

    server_settings = settings['server']

    user_control = UserControl(settings, db_manager)
    app.run(host = server_settings['host'], port = server_settings['port'])

if __name__ == '__main__':
    main()
