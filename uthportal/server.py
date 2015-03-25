import flask
from json import JSONEncoder

from multiprocessing import Process

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from operator import itemgetter

from logger import get_logger, logging_level

HTTPCODE_NOT_FOUND = 404
HTTPCODE_NOT_IMPLEMENTED = 501


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


app =  flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.json_encoder = BSONEncoderEx


@app.route('/inf/courses/all')
@app.route('/inf/courses')
def show_courses():
    db_manager = app.config['db_manager']
    db_courses = db_manager.find_documents('inf.courses')

    # Remove not needed keys #
    courses = [ ]
    for doc in sorted(db_courses,key=itemgetter('code')):
        del doc['announcements']
        del doc['_id']
        courses.append(doc)

    json = { 'children' : courses }
    return flask.jsonify(json)


@app.route('/inf/courses/<course_name>')
def show_course(course_name):
    db_manager = app.config['db_manager']
    db_doc = db_manager.find_document('inf.courses', {'code':course_name })

    if isinstance(db_doc, dict):
        db_doc = make_prod(db_doc)
        return flask.jsonify(db_doc)
    else:
        flask.abort(HTTPCODE_NOT_FOUND)

@app.route('/inf/announce/<type>')
def show_inf_announcements(type):
    db_manager = app.config['db_manager']
    db_doc = db_manager.find_document('inf.announce', {'type': type})

    if isinstance(db_doc, dict):
        db_doc = make_prod(db_doc)
        return flask.jsonify(db_doc)
    else:
        flask.abort(HTTPCODE_NOT_IMPLEMENTED)

@app.route('/inf/schedule')
def show_inf_schedule():
    db_manager = app.config['db_manager']
    db_doc = db_manager.find_document('inf.schedule')

    if isinstance(db_doc, dict):
        db_doc = make_prod(db_doc)
        return flask.jsonify(db_doc)
    else:
        flask.abort(HTTPCODE_NOT_IMPLEMENTED)

@app.route('/uth/rss/<type>')
def show_uth_announcements(type):
    db_manager = app.config['db_manager']
    db_doc = db_manager.find_document('uth.rss', {'type': type})

    if isinstance(db_doc, dict):
        db_doc = make_prod(db_doc)
        return flask.jsonify(db_doc)
    else:
        flask.abort(HTTPCODE_NOT_IMPLEMENTED)

@app.route('/uth/foodmenu')
def show_food_menu():
    db_manager = app.config['db_manager']

    _monday = (datetime.now() - timedelta(datetime.now().weekday())).date()
    last_monday = datetime.combine(_monday, datetime.min.time() )

    db_doc = db_manager.find_document('uth.food_menu', {'date':last_monday })

    if isinstance(db_doc, dict):
        db_doc = make_prod(db_doc)
        return flask.jsonify(db_doc)
    else:
        flask.abort(HTTPCODE_NOT_IMPLEMENTED)


def make_prod(doc):
    """
    Removed the unesseccery fields for production out.
    NOTE: Also removes 'last_updated' field in order for the client notifications to work
    """
    remove_fields = [ 'last_updated', '_id', 'announcements.last_updated' ]

    for field in remove_fields:
        path_to_field = field.split('.')

        tmp_doc = doc
        path_size = len(path_to_field)

        path_exists = True
        for node in path_to_field[:path_size-1]:
            if node in tmp_doc:
                tmp_doc = tmp_doc[node]
            else:
                path_exists = False
                break

        if path_exists and path_to_field[path_size-1] in tmp_doc:
            del tmp_doc[path_to_field[path_size-1]]

    return doc

def json_error(code, message):
    return flask.jsonify( {'error': {'code': code, 'message': message} } ), code

@app.errorhandler(HTTPCODE_NOT_FOUND)
def page_not_found(error):
    return json_error(HTTPCODE_NOT_FOUND,'Page not Found')

@app.errorhandler(HTTPCODE_NOT_IMPLEMENTED)
def not_implemented(error):
    return json_error(HTTPCODE_NOT_IMPLEMENTED,'Not implemented')



class Server(object):
    """
    An object-oriented wrapper for the flask-server
    """

    def __init__(self, database_manager, settings):
        self.logger = get_logger(__file__, logging_level.DEBUG)
        self.settings = settings
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


    def __start_flask(self):
        server_settings = self.settings['server']
        app.run(host = server_settings['host'], port = server_settings['port'])

