#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" gatherer.py: Contains Gatherer class which is the main uthportal project class.

Gatherer class contains all the logic to initialize and maintain the queue
as well as perform the neccessary operations on it.

In order to initialize the Gatherer class the following interfaces must be
passed as arguments:

    DatabaseManager: Interface for database operations
    PushNotificationManager: Interface for sending push notifications
                                (planning for Android & WP8.1 )
    *

"""

import tasks
import library.inf
import data.inf
import data.uth

class Scheduler(object):
    def __init__(self, tasks, apscheduler_kwargs, interval_dict):
        pass

    def add_task(name, func, interval=None):
        pass

    def remove_task(name):
        pass

    def init_queue(apscheduler_kwargs, interval_dict):
        pass

    def clear_queue():
        pass

