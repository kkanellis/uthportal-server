#!/usr/bin/env python

import sys
import unittest

from pkgutil import iter_modules
from importlib import import_module

TEST_PACKAGE = 'tests'
LINE_SPLIT = 70 * '-'

def explore_package(package_name):
    """
    Uses pkgutil to extract all modules from the requested package
    """
    return [name for (_, name, _) in iter_modules([package_name]) if name.startswith('test')]

def main():
    modules = ['%s.%s' % (TEST_PACKAGE, module) for module in explore_package(TEST_PACKAGE)]


    print 'Found modules: '
    print LINE_SPLIT
    for module in modules:
        print module
    print LINE_SPLIT + '\n\n'

    print 'Running tests:'
    print LINE_SPLIT

    testSuite = unittest.defaultTestLoader.loadTestsFromNames(modules)
    testRunner = unittest.TextTestRunner().run(testSuite)

if __name__ == "__main__":
    main()

