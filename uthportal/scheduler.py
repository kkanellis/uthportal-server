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
import gevent
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError, ConflictingIdError

from uthportal.logger import get_logger, logging_level

LINE_SPLITTER = 80 * '-'

class Scheduler(object):
    def __init__(self, tasks, intervals):
        self.logger = get_logger('scheduler', logging_level.DEBUG)

        if not isinstance(tasks, dict):
            self.logger.error('tasks is not a dictionary')
            return

        if not isinstance(intervals, dict):
            self.logger.error('intervals is not a dictionary')
            return

        self.tasks = self._flatten_dict(tasks, '')

        self.logger.debug('Tasks found:')
        self.logger.debug(LINE_SPLITTER)
        for key in self.tasks:
            self.logger.debug('%s\t|\t%s' % (key, self.tasks[key].task_type))
        self.logger.debug(LINE_SPLITTER)

        self.intervals = intervals

        #self.logger.debug('Checking tasks paths!')
        # TODO: Check if paths are valid

    def init(self, **apscheduler_kwargs):
        """ Initializes the queue, and adds the tasks """

        self.logger.info('Initilizing APScheduler...')

        ap_logger = get_logger('apscheduler', logging_level.DEBUG)
        self.sched = BackgroundScheduler(logger=ap_logger, **apscheduler_kwargs)

        for (id, task) in self.tasks.items():
            task_type = task.task_type

            self.logger.debug('Adding task "%s" [%s]' % (id, task_type))

            if not task_type in self.intervals:
                self.logger.warning('Interval not defined for "%s" class' % task_type)
                continue

            self.add_task(id, task, self.intervals[task_type])

        self.logger.info('APScheduler initialized!')

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
            if isinstance(interval, dict):
                self.sched.add_job(func, trigger='interval', id=id, **interval)
            elif interval is None: # Run once (ommit trigger)
                self.sched.add_job(func, id=id)
            else:
                self.logger.error('"interval" is not an instance of [time|None]')
                return
        except ConflictingIdError, e:
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

    def _flatten_dict(self, d, path):
        new_dict = { }
        for key in d:
            if isinstance(d[key], dict):
                new_path = '%s.%s' % (path, key) if path else key

                x = self._flatten_dict(d[key],new_path).copy()
                new_dict.update(x)
            else:
                new_key = '%s.%s' % (path, key)
                new_dict[new_key] = d[key]

        return new_dict
