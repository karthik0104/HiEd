"""
This class handles all the Social Network related operations across
the entire application. It is the central piece which connects all the social
networking activities such as discussion threads, user follow etc.
"""
from annotation.serializer import serialize_db_result
from config.argsparser import ArgumentsParser
from entity.discussion import DiscussionGroup
from entity.university import University
from exception.error_code import ErrorCode
from exception.field_exception import FieldException
from util.cassandra import CassandraConnection
from util.analytics import SpecificAnalytics
from entrypoint import db

configs = ArgumentsParser()
analytics = SpecificAnalytics()

class SocialService:
    #session = DataConnector.getSession(configs.db_host, configs.db_user, configs.db_password, configs.db_database)

    def createDiscussionGroup(self, current_user, data):
        if (data['university'] is None) or (len(data['university']) == 0):
            _discussion_group = DiscussionGroup(name=data['name'], description=data['description'])
        else:
            _university = db.session.query(University).filter_by(name=data['university']).first()
            if _university is None:
                raise FieldException(code=ErrorCode.FIELD_ERROR, message='University field invalid')

            _discussion_group = DiscussionGroup(name=data['group_name'], description=data['group_description'], university_id=_university.id)

        try:
            db.session.add(_discussion_group)
            db.session.commit()

            # Introduce metrics for the new discussion group
            analytics.store_discussion_group_metrics(_discussion_group.id)

            # Make the user a follower of the group if the user settings say so
            self.make_user_as_follower(current_user, _discussion_group.id)

        except Exception as e:
            print(e)
            db.session.rollback()

        return _discussion_group

    def make_user_as_follower(self, current_user, group_id):
        # TODO: Check if user settings has "auto-follow mode" enabled

        cassandra_connection = CassandraConnection()
        session = cassandra_connection.connect(keyspace='thread_ks')

        insert_query = self.prepare_query_for_making_user_as_follower(current_user.id, group_id)
        cassandra_connection.execute_query(insert_query, ['uuid', current_user.id, group_id, 'current_time'])

        return None

    def getDiscussionGroups(self, current_user, page_number):
        page_number = int(page_number) - 1
        page_size = configs.records_page_size

        filters = {}

        query = db.session.query(DiscussionGroup.id, DiscussionGroup.name.label('name'), DiscussionGroup.description,
                                 University.name.label('university_name')).\
            outerjoin(University, DiscussionGroup.university_id == University.id).filter_by(**filters)

        if page_size:
            query = query.limit(page_size)

        if page_number:
            query = query.offset(page_number * page_size)

        discussion_groups = query.all()

        discussion_groups_with_metrics = analytics.getDiscussionGroupsMetrics(discussion_groups)

        return discussion_groups_with_metrics


    def getDiscussionThreadsByGroup(self, current_user, group_id):
        """
        Return the discussion threads for the requested group
        :param current_user: Current logged in user
        :param group_id: Discussion threads of the requested group
        :return:
        """
        cassandra_connection = CassandraConnection()
        session = cassandra_connection.connect(keyspace='thread_ks')

        retrieve_query = self.prepare_query_for_retrieving_discussion_threads(group_id)
        query_result = cassandra_connection.execute_query(retrieve_query, records=None, query_type='RETRIEVE')
        discussion_threads = query_result._current_rows

        return discussion_threads.to_dict('records')

    def getThreadRepliesByDiscussionThread(self, current_user, discussion_thread_id):
        """
        Return the thread replies for the requested discussion thread
        :param current_user: Current logged in user
        :param discussion_thread_id: Thread replies of the requested discussion thread
        :return:
        """
        cassandra_connection = CassandraConnection()
        cassandra_connection.connect(keyspace='thread_ks')

        retrieve_query = self.prepare_query_for_retrieving_thread_replies(discussion_thread_id)
        thread_replies = cassandra_connection.execute_query(retrieve_query, records=None, query_type='RETRIEVE')._current_rows

        return thread_replies

    def addDiscussionThread(self, title, content):
        """
        Add a new dicsussion thread
        :param title: The title of the discussion thread
        :param content: The content of the dicsussion thread
        """
        cassandra_connection = CassandraConnection()
        session = cassandra_connection.connect(keyspace='thread_ks')

        insert_query = self.prepare_query_for_inserting_discussion_thread()
        cassandra_connection.execute_query(insert_query, ['uuid', 1, 1, title, content, 'current_time'])

    def addThreadReply(self, content, discussion_thread_id):
        """
        Add a new thread reply to the discussion thread
        :param content: The content of the reply
        :param discussion_thread_id: The reply to the discussion thread in which the reply has to be added
        """
        cassandra_connection = CassandraConnection()
        cassandra_connection.connect(keyspace='thread_ks')

        insert_query = self.prepare_query_for_inserting_thread_reply()
        cassandra_connection.execute_query(insert_query, ['uuid', discussion_thread_id, 1, content, 'current_time'])

    def prepare_query_for_inserting_discussion_thread(self):
        query = "INSERT INTO discussion_thread (id, group_id, user_id, title, content, time1) VALUES (?, ?, ?, ?, ?, ?)"
        return query

    def prepare_query_for_inserting_thread_reply(self):
        query = "INSERT INTO thread_reply (id, discussion_thread_id, user_id, content, time1) VALUES (?, ?, ?, ?, ?)"
        return query

    def prepare_query_for_retrieving_discussion_threads(self, group_id):
        query = "SELECT * FROM discussion_thread WHERE group_id=" + str(group_id)
        return query

    def prepare_query_for_retrieving_thread_replies(self, discussion_thread_id):
        query = "SELECT * FROM thread_reply WHERE discussion_thread_id=" + str(discussion_thread_id)
        return query

    def prepare_query_for_making_user_as_follower(self):
        query = "INSERT INTO group_follower (id, group_id, user_id, time1) VALUES (?, ?, ?, ?)"
        return query

#ss = SocialService()
#dt = ss.getDiscussionThreadsByGroup(None, 1)
#df = dt._current_rows