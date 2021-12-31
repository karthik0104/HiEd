"""
This is the Cassandra connector class for managing all the high-performance read
operations. Cassandra is mainly being used in this application for handling
Discussion Thread operations.
"""
import cassandra.util
import pandas as pd
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT, ConsistencyLevel
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory, SimpleStatement
import uuid
import datetime
from config.argsparser import ArgumentsParser

class CassandraConnection:

    cluster = None
    session = None

    args = ArgumentsParser()

    def __init__(self):

        def pandas_factory(colnames, rows):
            return pd.DataFrame(rows, columns=colnames)

        profile = ExecutionProfile(
            load_balancing_policy=WhiteListRoundRobinPolicy([self.args.cassandra_host]),
            retry_policy=DowngradingConsistencyRetryPolicy(),
            consistency_level=ConsistencyLevel.LOCAL_QUORUM,
            serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
            request_timeout=15,
            row_factory=pandas_factory
        )

        if CassandraConnection.cluster is None:
            CassandraConnection.cluster = Cluster(execution_profiles={EXEC_PROFILE_DEFAULT: profile}, port=self.args.cassandra_port)

    def connect(self, keyspace):
        if CassandraConnection.session is None:
            CassandraConnection.session = self.cluster.connect()
            CassandraConnection.session.set_keyspace(keyspace)
            CassandraConnection.session.default_fetch_size = None

        #print(session.execute("SELECT release_version FROM system.local").one())

        return CassandraConnection.session

    def execute_query(self, query, records=None, query_type='ADD'):
        statement = CassandraConnection.session.prepare(query)

        # Handle UUID values
        if records is not None:
            records = [cassandra.util.uuid_from_time(datetime.datetime.now()) if _ == 'current_time' else uuid.uuid1() if _ == 'uuid'
            else _ for _ in records]

        if query_type == 'ADD':
            results = CassandraConnection.session.execute(statement, records)
        else:
            results = CassandraConnection.session.execute(statement)

        return results