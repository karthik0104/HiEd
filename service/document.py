"""
This is the service layer which caters to providing save and auto-save functionality of documents, and communicating
with the database.
"""
from bson import ObjectId

import entity.user
from annotation.security import token_required
from entity.user import User
from exception.error_code import ErrorCode
from exception.field_exception import FieldException
from util import diff_match_patch as dmp_module
from util.mongodb import MongoConnection
from util.redis import RedisConnection
from annotation.deprecated import deprecated
import threading
import re

from config.argsparser import ArgumentsParser

configs = ArgumentsParser()
dmp = dmp_module.diff_match_patch()

class DocumentService:

    # Below objects are common throughout the application, hence need to be carefully dealt with
    redis_pipeline = {}
    redis_pipeline_lock = {}

    TIME_PREFIX = "\[time:[0-9]*\.[0-9]*\]"
    PATCH_PREFIX = "\[patch\]"
    UPDATE_PREFIX = "\[update\]"

    def __init__(self):
        self.dmp = dmp_module.diff_match_patch()
        self.mongo_connection = MongoConnection(configs.mongo_username, configs.mongo_password, configs.mongo_server, configs.mongo_database)
        self.db = self.mongo_connection.connect()
        self.document_collection = self.mongo_connection.get_collection(configs.mongo_document_collection)
        self.diff_document_collection = self.mongo_connection.get_collection(configs.mongo_diff_document_collection)
        self.redis_connection = RedisConnection(configs.redis_host, configs.redis_port, configs.redis_password)
        self.redis = self.redis_connection.get_connection()


    @deprecated
    def create_document_db(self, current_user: entity.user.User):
        """
        Service method to create a new document and save it in the database
        :param current_user: The user creating the new document
        """
        document_id = self.mongo_connection.add_document(self.document_collection, {'content': ''})
        return {'document_id': str(document_id)}

    @deprecated
    def save_diff_db(self, current_user: entity.user.User, document_id: str, changes:str, is_patch: bool) -> bool:
        """
        Service method to save the diff changes received for the document
        :param current_user: The user requesting the changes
        :param document_id: The document id for which the change is requested
        :param changes: The diff changes received
        :param is_patch: If the request is a patch one or replace one
        :return: Whether the diff save was successful or not
        """
        document = self.check_document_access(current_user, document_id)
        if document is None:
            raise FieldException(code=ErrorCode.NO_DOCUMENT,
                                 message='Either document does not exist or User is not authorized to access this document')

        diff_document = {
            'author': current_user.id,
            'document_key': document_id,
            'is_patch': is_patch,
            'is_processed': False,
            'diff': changes
        }

        self.mongo_connection.add_document(self.diff_document_collection, diff_document)

        return True

    @deprecated
    def apply_diff_db(self, current_user: entity.user.User, document_id: str) -> bool:
        """
        Service method to apply the diff changes to be applied for the document
        :param current_user: The user requesting the changes
        :param document_id: The document id for which the change is requested
        :return: Whether the diff application was successful or not
        """
        document = self.check_document_access(current_user, document_id)
        if document is None:
            raise FieldException(code=ErrorCode.NO_DOCUMENT,
                                 message='Either document does not exist or User is not authorized to access this document')

        required_diffs = self.mongo_connection.find_by_fields(self.diff_document_collection, {'document_key': document_id,
                                                                                             'is_processed': False})

        original_text = document['content']
        updated_text = self.perform_recursive_diff_db(original_text, required_diffs)

        self.mongo_connection.find_by_fields_and_update(self.document_collection, {'_id': ObjectId(document_id)}, 'content', updated_text)

        # Get the updated document
        document = self.check_document_access(current_user, document_id)

        return document

    @deprecated
    def perform_recursive_diff_db(self, original_text, required_diffs):
        """
        Utility method to perform recursive diff on the document
        :param original_text: The original text contained in the document
        :param required_diffs: The set of diff objects to apply
        :return: The updated text after all the diffs have been applied
        """
        updated_text = None

        for diff in required_diffs:
            if diff['is_patch'] and (diff['is_processed'] is False):
                patch_text = diff['diff']
                patch = dmp.patch_fromText(patch_text)

                if updated_text is None:
                    updated_text = dmp.patch_apply(patch, original_text)[0]
                else:
                    updated_text = dmp.patch_apply(patch, updated_text)[0]
            else:
                updated_text = diff['diff']

            self.mongo_connection.find_by_fields_and_update(self.diff_document_collection, {'_id': diff['_id']}, 'is_processed', True)

        return updated_text


    def create_document(self, current_user: entity.user.User):
        """
        Service method to create a new document and save it in the database
        :param current_user: The user creating the new document
        """
        document_id = self.mongo_connection.add_document(self.document_collection, {'content': ''})

        # Initialize the redis pipeline for the document, and the re-entrant lock for protecting the pipeline object
        self.redis_pipeline[str(document_id)] = self.redis_connection.get_pipeline(self.redis)
        self.redis_pipeline_lock[str(document_id)] = threading.RLock()

        return {'document_id': str(document_id)}


    def save_diff(self, current_user: entity.user.User, document_id: str, changes:str, is_patch: bool) -> bool:
        """
        Service method to save the diff changes received for the document
        :param current_user: The user requesting the changes
        :param document_id: The document id for which the change is requested
        :param changes: The diff changes received
        :param is_patch: If the request is a patch one or replace one
        :return: Whether the diff save was successful or not
        """
        document = self.check_document_access(current_user, document_id)
        if document is None:
            raise FieldException(code=ErrorCode.NO_DOCUMENT,
                                 message='Either document does not exist or User is not authorized to access this document')

        if is_patch:
            self.redis_connection.save_in_sorted_set_with_timestamp(self.redis_pipeline[document_id], document_id, changes, self.PATCH_PREFIX)
        else:
            self.redis_connection.save_in_sorted_set_with_timestamp(self.redis_pipeline[document_id], document_id, changes, self.UPDATE_PREFIX)

        if self.should_push_to_redis_immediate(self.redis_pipeline[document_id]):
            self.redis_connection.execute_pipeline(self.redis_pipeline[document_id])

        return True

    def should_push_to_redis_immediate(self, pipeline):
        """
        Inspect conditions based on priority order and decide when to push to Redis server
        :param pipeline: The specific Redis pipeline
        :return: Whether to push to redis immediately or not
        """
        return True

    def apply_diff(self, current_user: entity.user.User, document_id: str) -> bool:
        """
        Service method to apply the diff changes to be applied for the document
        :param current_user: The user requesting the changes
        :param document_id: The document id for which the change is requested
        :return: Whether the diff application was successful or not
        """
        document = self.check_document_access(current_user, document_id)
        if document is None:
            raise FieldException(code=ErrorCode.NO_DOCUMENT,
                                 message='Either document does not exist or User is not authorized to access this document')

        required_diffs = self.get_diff_docs_for_document(document_id)

        original_text = document['content']
        updated_text = self.perform_recursive_diff(document_id, original_text, required_diffs)

        self.mongo_connection.find_by_fields_and_update(self.document_collection, {'_id': ObjectId(document_id)}, 'content', updated_text)

        # Get the updated document
        document = self.check_document_access(current_user, document_id)

        return document

    def get_diff_docs_for_document(self, document_id):
        """
        Return the diff texts for the document
        :param document_id: The document id
        :return: The byte string messages stored on Redis
        """
        encoded_messages = self.redis.zscan(document_id)[1]
        return encoded_messages

    def perform_recursive_diff(self, document_id, original_text, required_diffs):
        """
        Utility method to perform recursive diff on the document
        :param original_text: The original text contained in the document
        :param required_diffs: The set of diff objects to apply
        :return: The updated text after all the diffs have been applied
        """

        def remove_prefix(text, prefix):
            return re.sub(text, '', prefix)

        updated_text = None

        for diff in required_diffs:
            diff = remove_prefix(self.TIME_PREFIX, diff[0].decode('utf-8'))

            if self.is_diff_patch(diff):
                patch_text = self.get_patch_text(diff)

                patch = dmp.patch_fromText(patch_text)

                if updated_text is None:
                    updated_text = dmp.patch_apply(patch, original_text)[0]
                else:
                    updated_text = dmp.patch_apply(patch, updated_text)[0]
            else:
                updated_text = self.get_update_text(diff)

            self.redis.zrem(document_id, diff)

        return updated_text

    def is_diff_patch(self, diff):
        return bool(re.search(self.PATCH_PREFIX, diff))

    def get_patch_text(self, diff):
        return re.sub(self.PATCH_PREFIX, '', diff).lstrip()

    def get_update_text(self, diff):
        return re.sub(self.UPDATE_PREFIX, '', diff).lstrip()

    def apply_patch(self, document_text: str, patch_text: str):
        """
        Utility method to apply patch on the document
        :param document_id: The document id
        :param patch: The diff received for the document
        :return:
        """
        patch = self.dmp.patch_fromText(patch_text)
        updated_text = self.dmp.patch_apply(document_text, patch)

        return updated_text

    def check_document_access(self, user: entity.user.User, document_id: str) -> bool:
        """
        Utility method to check document access for the logged in user
        :param user:
        :param document_id:
        :return:
        """
        document = self.mongo_connection.find_by_fields(self.document_collection, {'_id': ObjectId(document_id)}, multiple=False)

        return document

    def replace_document(self, document_id: int, changes: str) -> bool:
        """
        Utility method to update the document with the new content
        :param document_id:
        :param changes:
        :return:
        """
        return True