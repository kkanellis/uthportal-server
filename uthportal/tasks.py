#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" tasks.py: Holds all classes used by gatherer to make uthportal work.

Base class is an abstract class named BaseTask. BaseTask holds all
common methods and properties need to be implemented.

Currently working classes are:
    *

"""

from abc import ABCMeta, abstractmethod

class BaseTask(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def save(self):
        pass

    def load(self):
        pass

    @abstractmethod
    def load_first(self):
        pass

    @abstractmethod
    def __call__(self):
        pass

class InfCourse(BaseTask):
    pass

