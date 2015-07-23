#!/bin/env/python
# -*- coding: utf-8 -*-

info = """
Module for testing individual tasks. Very usefull when writing new tasks or fixing the existing ones

Usage: checktask.py path_to_task output_file[optional]
e.g    checktask.py inf.announce.general data.json
e.g2   checktask.py inf.courses.ceXXX
"""

GREEN_TICK = "\033[1;32m✔\033[0m"
RED_CROSS = "\033[1;31m✘\033[0m"


#this dictionary provides a list of fields to check for each type of task
#to get all types of tasks use 'tree uthportal/library -I *.pyc'

FIELDS_DICT = {
        "inf.courses" : ['announcements.eclass', 'announcements.site'],
        "inf.announce" : ['entries'],
        "uth.announce" : ['entries'],
        "uth.food" : ['menu'],
        }

import sys
from os.path import abspath, dirname
from pkgutil import get_loader
from inspect import isclass, getmembers
from json import dumps, JSONEncoder

from uthportal.database.memory import MemoryDatabaseManager
from uthportal.configure import Configuration
from uthportal.util import BSONEncoderEx

def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print 'Invalid number of arguments [%d]' % len(sys.argv)
        print info
        return

    if sys.argv[1] in ['help', '-h', '--help']:
        print info
        return

    dot_path = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) == 3 else None

    # Get setings and init db_manager
    config = Configuration()
    settings = config.get_settings()

    db_manager = MemoryDatabaseManager()

    # Construct path & module name
    spath = dot_path.split('.')

    task_type = '.'.join(spath[:-1])
    if task_type not in FIELDS_DICT:
        print 'Invalid task!'
        return

    path = settings['library_path'] + '/' + '/'.join(spath)
    classname = spath[-1]

    # Retrieve task class
    task_class = None
    loader = get_loader(path)

    if not loader:
        print 'Unable to find module: ' + path
        print 'Make sure it exists'
        return

    module = loader.load_module(classname)

    if not module:
        print 'Unable to import module: ' + path
        return

    for name, object in getmembers(module):
        if isclass(object) and name == classname:
            task_class = object
            break

    if not task_class:
        print 'Unable to import task: ' + path
        return

    print '\n\nTask type: [%s], Task name: [%s]' %( task_type, classname)
    print 'Press Enter to continue'
    raw_input()

    # Initialize & call the task
    print '\nInitiallizing task...'
    task_instance = task_class('.'.join(spath), path, settings, db_manager)
    print '\nRunning task...'
    task_instance.__call__()

    # Contruct the data dictionary
    result = { }
    for field in task_instance.update_fields:
        result[field] = task_instance._get_document_field(task_instance.document, field)

    print "\nDone...\nResults:"
    print "======================================"
    #Check if fields exist and are not empty
    fields_to_check = FIELDS_DICT[task_type]
    for field in fields_to_check:
        if field in result and result[field]:
            print "%s: [%s]" %(field, GREEN_TICK)
        else :
            print "%s: [%s]" %(field, RED_CROSS)


    # Pretty print the data
    data = dumps(
            result,
            cls=BSONEncoderEx,
            sort_keys=True,
            ensure_ascii=False,
            indent=4
        )

#    print data

        # Write to file (if have to)
    if out_file:
        with open(out_file, 'w') as f:
            f.write(data.encode('utf8'))


if __name__ == '__main__':
    main()
