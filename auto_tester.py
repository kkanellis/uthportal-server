#!/usr/bin/env python

import sys
from pkgutil import iter_modules
from importlib import import_module
TEST_PACKAGE = 'test'

def explore_package(package_name):
    """
    Uses pkgutil to extract all modules from the requested package
    """
    return [name for x, name, y in iter_modules([package_name])]

def main():
    modules = explore_package(TEST_PACKAGE)

    #Import each module and extract it's main function, then call it.
    for i, module in enumerate(modules):
        print("[%s]: Running test: [ %s ]..." % (i, module))
        imported_module = import_module("%s.%s" % (TEST_PACKAGE,module) )

        if imported_module is None:
            print("Cannot import module")
            continue

        imported_main = getattr(imported_module, 'main')

        if imported_module is None:
            print("ERROR: Module %s doesn't contain a main function" % str(module))
            continue

        if imported_main() :
            print("\tSuccess!")
        else :
            print(" \tFailure")

if __name__ == "__main__":
    main()
