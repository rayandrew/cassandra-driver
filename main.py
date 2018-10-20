#!/usr/bin/env python

from __future__ import print_function

from utils.Connection import Connection
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--migration', type=str, nargs='?', default='',
                    help='Specifiy a migration action [up, down]')
parser.add_argument('--seed', type=str, nargs='?', default='',
                    help='Specifiy a seed action [up, down]')
parser.add_argument('--table', type=str, nargs='?', default='',
                    help='Specify table action [create, drop]')
parser.add_argument('--create', nargs='+', type=str,
                    help='Create new migration/seeds file [migration, seed [name]]')
parser.add_argument('--query', nargs='+', type=str,
                    help='Querying database')

import pprint

pp = pprint.PrettyPrinter(indent=2)

KEYSPACE = "rayandrew"

cassandra = Connection(
    cluster=["167.205.35.19", "167.205.35.20",
             "167.205.35.21", "167.205.35.22"],
    keyspace="rayandrew",
    connect_timeout=50)


def create_migration():
    import shutil
    import time
    import datetime

    now = str(int(time.mktime(datetime.datetime.now().timetuple())))

    src_dir = "./utils/migration.template"
    dst_dir = "./migrations/" + now + "_migration.py"
    shutil.copy(src_dir, dst_dir)


def create_seed(name):
    import shutil

    src_dir = "./utils/seed.template"
    dst_dir = "./seeds/" + name + "_seeds.py"
    shutil.copy(src_dir, dst_dir)


def migration_up(conn):
    from migrations.__init__ import __load_migrations_up__
    __load_migrations_up__(conn)


def migration_down(conn):
    from migrations.__init__ import __load_migrations_down__
    __load_migrations_down__(conn)


def seed_up(conn):
    from seeds.__init__ import __load_seeds_up__
    __load_seeds_up__(conn)


def seed_down(conn):
    from seeds.__init__ import __load_seeds_down__
    __load_seeds_down__(conn)


if __name__ == "__main__":
    print('Started')
    args = parser.parse_args()

    # if args.query is not None:
    #     cassandra.execute(args.query)

    if args.migration == 'up':
        migration_up(cassandra)
    elif args.migration == 'down':
        migration_down(cassandra)

    if args.seed == 'up':
        seed_up(cassandra)
    elif args.seed == 'down':
        seed_down(cassandra)

    if args.create is not None:
        if args.create[0] == 'migration':
            create_migration()
        elif args.create[0] == 'seed':
            create_seed(args.create[1])

    if args.table == 'create':
        print('Creating table...')
        cassandra.migrate_table('./create_table.csql')
    elif args.table == 'drop':
        print('Dropping table...')
        cassandra.migrate_table('./drop_table.csql')

    cassandra.shutdown()
    print('Finished')
