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

from logger import get_logger, logging_level

import gevent
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError, ConflictingIdError

class Scheduler(object):
    def __init__(self, tasks, apscheduler_kwargs, intervals):
        import inspect
        name = inspect.stack()[0][1] #get filename

        self.logger = get_logger(name, logging_level.DEBUG)

        if not isinstance(tasks, dict):
            self.logger.error('tasks arg not a dictionary')
            return

        self.tasks = tasks
        self.intervals = intervals

        self.logger.debug('Checking tasks paths!')
        # TODO: Check if paths are valid
        self.init(apscheduler_kwargs)

    def init(self, apscheduler_kwargs):
        """ Initializes the queue, and adds the tasks """

        self.sched = BackgroundScheduler(apscheduler_kwargs, logger=logger)

        for dept in self.tasks:
            for task in self.tasks[dept]:
                _class = self.tasks[dept][task]
                _class_str = str(type(_class))

                if not _class_str in self.intervals:
                    self.logger.warning('Interval not defined for "%s" class' % _class_str)
                    continue

                id = '%s.%s' % (dept, task)
                self.add_task(id, _class, self.intervals[_class_str])

        self.start()

    def clear(self):
        """ Removes all jobs from scheduler """
        if not isinstance(self.sched, BaseScheduler):
            self.logger.error('Scheduler is not initialized')
            return

        for job in self.sched.get_jobs():
            job.remove()

    def start(self):
        """ Start the scheduler by starting the instance of APScheduler """
        if not isinstance(self.sched, BaseScheduler):
            self.logger.error('Scheduler is not initialized')
            return

        try:
            self.sched.start()
        except SchedulerAlreadyRunningError, e:
            self.logger.warning(e)


    def stop(self, wait=True):
        """ Stop the scheduler. If wait=True, then it will be stopped after
            all jobs that are currently executed will finish """
        if not isinstance(self.sched, BaseScheduler):
            self.logger.warning('Scheduler is not initialized')
            return

        try:
            self.sched.shutdown(wait=wait)
        except SchedulerNotRunningError, e:
            self.logger.warning(e)

    def add_task(self, id, func, interval=None):
        """ Adds a new task into the queue. If interval is None then the task
            will be executed once. """
        if not isinstance(id, basestring):
            self.logger.error('"id" argument is not an instance of basestring')
            return

        if not hasattr(func, '__call__'):
            self.logger.error('"func" is not callable')
            return

        try:
            if isinstance(interval, datetime):
                self.sched.add_job(func, 'interval', id, interval)
            elif isinstace is None: # Run once (ommit trigger)
                self.sched.add_job(func, id=id)
            else:
                self.logger.error('"interval" is not an instance of [datetime|None]')
                return
        except ConfilictingIdError, e:
            self.logger.warning(e)

    def remove_task(self, id):
        """ Remove a job from the queue """
        if not isinstance(id, basestring):
            self.logger.error('"id" argument is not an instance of basestring')
            return

        try:
            self.sched.remove_job(id)
        except JobLookupError, e:
            self.logger.warning(e)


if __name__ == '__main__':

    sched = Scheduler({ }, { }, { })
    sched.stop()

