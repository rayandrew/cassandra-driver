import imp
import os
# import asyncio

from faker import Faker

import time

fake = Faker()

NUMBER_GENERATOR = 5

dir = "seeds"

list_modules = sorted(os.listdir(dir))
list_modules.remove('__init__.py')


def __load_seeds_up__(session):
    print("Run seeding up...")
    for module_name in list_modules:
        if module_name.split('.')[-1] == 'py':
            print("Running from " + module_name)
            foo = imp.load_source('module', dir+os.sep+module_name)
            foo.up(session)


def __load_seeds_down__(session):
    print("Run seeding down...")
    for module_name in list_modules:
        if module_name.split('.')[-1] == 'py':
            print("Running from " + module_name)
            foo = imp.load_source('module', dir+os.sep+module_name)
            foo.down(session)
