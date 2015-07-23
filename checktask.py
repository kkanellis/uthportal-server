#!/bin/env/python
# -*- coding: utf-8 -*-

info = """
Module for testing individual tasks. Very usefull when writing new tasks or fixing the existing ones

Usage: checktask.py path_to_task output_file[optional]
e.g    checktask.py inf.announce.general data.json
e.g2   checktask.py inf.courses.ceXXX
"""

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

    # Initialize & call the task
    task_instance = task_class('.'.join(spath), path, settings, db_manager)
    task_instance.__call__()

    # Contruct the data dictionary
    result = { }
    for field in task_instance.update_fields:
        result[field] = task_instance._get_document_field(task_instance.document, field)

    # Pretty print the data
    data = dumps(
            result,
            cls=BSONEncoderEx,
            sort_keys=True,
            ensure_ascii=False,
            indent=4
        )

    print data

    # Write to file (if have to)
    if out_file:
        with open(out_file, 'w') as f:
            f.write(data.encode('utf8'))


if __name__ == '__main__':
    main()
