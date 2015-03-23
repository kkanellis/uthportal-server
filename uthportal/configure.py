""" Settings used for UTHPortal """

from datetime import time

settings = {
        'database': {
            'host': 'localhost',
            'port': 27017,
            'db_name': 'uthportal'
        },
        'scheduler' : {
            'apscheduler' : { },
            'intervals' : {
                'CourseTask' : { 'minutes' : 5 },
                'FoodmenuTask': { 'hours' : 1 }
            }
        },
        'server' : {
            'host' : '127.0.0.1',
            'port' : 5000,
        },
        'library_path' : 'uthportal/library'
}

