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



class Server(object):
    def __init__(self, database_manager, settings):
        self.logger = get_logger(__file__, logging_level.DEBUG)
        self.settings = settings
        self.__database_manager = database_manager

        self.__process = None
        self.__is_running = False

        app.config['server'] = self #ultrahax

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

    @app.route('/inf/courses/all')
    @app.route('/inf/courses')
    def show_courses():
        self = app.config['server']
        db_courses = self.__database_manager.find_documents('inf.courses')

        # Remove not needed keys #
        courses = [ ]
        for doc in sorted(db_courses,key=itemgetter('code')):
            del doc['announcements']
            del doc['_id']
            courses.append(doc)

        json = { 'children' : courses }
        return flask.jsonify(json)


