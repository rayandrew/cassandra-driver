import imp
import os

dir = "migrations"

list_modules = sorted(os.listdir(dir))
list_modules.remove('__init__.py')


def __load_migrations_up__(session):
    print("Run migrations up...")
    for module_name in list_modules:
        if module_name.split('.')[-1] == 'py':
            print("Running from " + module_name)
            foo = imp.load_source('module', dir + os.sep+module_name)
            foo.up(session)


def __load_migrations_down__(session):
    print("Run migrations down...")
    for module_name in list_modules:
        if module_name.split('.')[-1] == 'py':
            print("Running from " + module_name)
            foo = imp.load_source('module', dir + os.sep+module_name)
            foo.down(session)
