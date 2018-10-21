from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement, BatchStatement
from cassandra.policies import RetryPolicy
import logging
import time
import datetime

DEFAULT_CLUSTER = ["127.0.0.1"]
TYPE_OF_DROP = ["TABLE", "MATERIALIZED VIEW", "VIEW"]

KEYSPACE = "default"


class Connection():
    def __init__(self, cluster=DEFAULT_CLUSTER, keyspace=KEYSPACE, **kwargs):
        unixtime = str(int(time.mktime(datetime.datetime.now().timetuple())))

        logging.basicConfig(
            filename='./logs/' + unixtime + '_driver_cassandra.log', level=logging.DEBUG)
        self.log = logging.getLogger()
        self.log.setLevel('DEBUG')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

        self.cluster = Cluster(cluster, **kwargs)
        self.session = self.cluster.connect()

        self._batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        self.log.info("Setting keyspace...")
        self.session.set_keyspace(keyspace)

    def shutdown(self):
        self.cluster.shutdown()
        return self

    @property
    def consistency_level(self):
        return ConsistencyLevel

    @property
    def batch_statement(self):
        return self._batch

    def migrate_table(self, filename):
        self.log.info("Migrate table...")
        tables = self.read_csql(filename)
        for table in tables:
            print(table)
            self.session.execute(table)

    def prepare_statement(self, statement):
        return self.session.prepare(statement)

    def prepare_simple_statement(self, statement, **kwargs):
        return SimpleStatement(statement, **kwargs)

    def prepare_batch_statement(self, query, dic=None, **kwargs):
        self._batch.add(query, dic, **kwargs)
        return self._batch

    def empty_batch_statement(self):
        self._batch.clear()
        return self._batch

    def execute(self, query, dic=None, **kwargs):
        return self.session.execute(query, dic, **kwargs)

    def execute_async(self, query, **kwargs):
        return self.session.execute_async(query, **kwargs)

    def drop(self, name, type=TYPE_OF_DROP[0]):
        assert type in TYPE_OF_DROP
        self.session.execute("DROP " + type + " " + name)

    def truncate(self, tablename):
        self.session.execute("TRUNCATE " + tablename)

    def read_csql(self, filename):
        with open(filename) as file:
            return [x for x in file.read().replace("\n", "").split("=") if x]
