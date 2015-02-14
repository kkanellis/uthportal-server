#!/usr/bin/env python

import sys
import unittest

from pkgutil import iter_modules
from importlib import import_module
TEST_PACKAGE = 'tests'

def explore_package(package_name):
    """
    Uses pkgutil to extract all modules from the requested package
    """
    return [name for x, name, y in iter_modules([package_name])]

def main():
    modules = ['%s.%s' % (TEST_PACKAGE, module) for module in explore_package(TEST_PACKAGE)]

    testSuite = unittest.defaultTestLoader.loadTestsFromNames(modules)
    testRunner = unittest.TextTestRunner().run(testSuite)

if __name__ == "__main__":
    main()

