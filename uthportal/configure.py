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
                'CourseTask' : { 'minutes' : 10 },
                'FoodmenuTask': { 'hours' : 1 }
            }
        },
        'library_path' : 'uthportal/library'
}

