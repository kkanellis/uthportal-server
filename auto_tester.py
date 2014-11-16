import sys
from pkgutil import iter_modules
from importlib import import_module

def explore_package(package_name):
    """
    Uses pkgutil to extract all modules from the requested package
    """
    return [name for x, name, y in iter_modules([package_name])]

def main():
    modules = explore_package('test')
    #Import each module and extract it's main function, the call it.
    for i, module in enumerate(modules):
        print("[%s]: Testing module %s" % (i, module))
        imported_module = import_module("test." + module)

        if imported_module is None:
            print("Cannot import module")
            continue

        imported_main = getattr(imported_module, 'main')

        if imported_module is None:
            print("Module %s doesn't contain a main function" % str(module))
            continue

        imported_main()

if __name__ == "__main__":
    main()




