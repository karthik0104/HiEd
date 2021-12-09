"""
This is the Cassandra connector class for managing all the high-performance read
operations. Cassandra is mainly being used in this application for handling
Discussion Thread operations.
"""
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT, ConsistencyLevel
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory, SimpleStatement
import uuid
import datetime
from config.argsparser import ArgumentsParser

class CassandraConnection:

    cluster = None
    args = ArgumentsParser()

    def __init__(self):
        profile = ExecutionProfile(
            load_balancing_policy=WhiteListRoundRobinPolicy([self.args.cassandra_host]),
            retry_policy=DowngradingConsistencyRetryPolicy(),
            consistency_level=ConsistencyLevel.LOCAL_QUORUM,
            serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
            request_timeout=15,
            row_factory=tuple_factory
        )
        self.cluster = Cluster(execution_profiles={EXEC_PROFILE_DEFAULT: profile}, port=self.args.cassandra_port)

    def connect(self, keyspace):
        session = self.cluster.connect()
        session.set_keyspace(keyspace)
        print(session.execute("SELECT release_version FROM system.local").one())

        return session

    def insert_records(self, session, records):
        statement = session.prepare("INSERT INTO thread (id, participants, created_at) VALUES (?, ?, ?)")
        results = session.execute(statement, records)

# USAGE
#cassandra_connection = CassandraConnection()
#session = cassandra_connection.connect(keyspace='thread_ks')
#cassandra_connection.insert_records(session, [uuid.uuid1(), [], datetime.datetime(year=2021, month=9, day=12)])