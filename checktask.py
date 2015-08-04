#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

info = """
Module for testing individual tasks.
Very useful when writing new tasks or
fixing the existing ones.
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
        "inf" : ['entries' ]
        }

import sys
from argparse import ArgumentParser
from os.path import abspath, dirname
from pkgutil import get_loader
from inspect import isclass, getmembers
from json import dumps, JSONEncoder

from uthportal.database.memory import MemoryDatabaseManager
from uthportal.configure import Configuration
from uthportal.util import BSONEncoderEx


def check_task(task_path, presult = False, outfile = None):
    dot_path = task_path

    # Get setings and init db_manager
    config = Configuration()
    settings = config.get_settings()

    db_manager = MemoryDatabaseManager()

    # Construct path & module name
    spath = dot_path.split('.')

    task_type = '.'.join(spath[:-1])
    if task_type not in FIELDS_DICT:
        print 'Invalid task type, or only type given'
        print 'Your input was: [%s]' % dot_path
        print 'Valid task types are: \n\t%s' % "\n\t".join(FIELDS_DICT.keys())
        sys.exit(1)

    path = 'uthportal/' + settings['library_path'] + '/' + '/'.join(spath)
    classname = spath[-1]

    # Retrieve task class
    task_class = None
    loader = get_loader(path)

    if not loader:
        print 'Unable to find module: ' + classname
        print 'Make sure it exists'
        return

    module = loader.load_module(classname)

    if not module:
        print 'Unable to import module: ' + dot_path
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
    task_instance = task_class('.'.join(spath), settings, db_manager)
    print '\nRunning task...'
    task_instance.__call__()

    # Contruct the data dictionary
    result = { }
    for field in task_instance.update_fields:
        result[field] = task_instance._get_document_field(task_instance.document, field)

    #Prettify result data
    data = dumps(
            result,
            cls=BSONEncoderEx,
            sort_keys=True,
            ensure_ascii=False,
            indent=4
        )


    if presult:
        print "\n=============================================================="
        print "Actual returned data:"
        print "==============================================================\n"
        print data
        print "\n=============================================================="

    print "\nDone...\nResults:"
    print "======================================"

    #Check if fields exist and are not empty
    fields_to_check = FIELDS_DICT[task_type]
    for field in fields_to_check:
        if field in result and result[field]:
            print "%s: [%s]" %(field, GREEN_TICK)
        else :
            print "%s: [%s]" %(field, RED_CROSS)

    if outfile:
        print "\nWriting data to file: [%s]..." % outfile[0]
        with open(outfile[0], 'w') as f:
            f.write(data.encode('utf8'))

def main():

    parser = ArgumentParser(description = info)
    parser.add_argument("module_name", help="The name of the module to test",
            metavar = "module name", type = str)
    parser.add_argument("-o","--outfile", help="Output result data in the specified file", type = str, nargs = 1)
    parser.add_argument("-p", "--presult", help="Print the whole result", action="store_true")
    args = parser.parse_args()

    check_task(args.module_name, args.presult, args.outfile)

    print "\nBye :)"
if __name__ == '__main__':
    main()
