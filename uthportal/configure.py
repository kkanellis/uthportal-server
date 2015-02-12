""" Settings used for UTHPortal """

from datetime import time

settings = {
        'scheduler' : {
            'apscheduler' : { },
            'intervals:' : {
                'CourseTask' : time(minute=10),
                'FoodmenuTask': time(hour=1)
            }
        }
}


