"""
This is the service layer which caters to providing save and auto-save functionality of documents, and communicating
with the database.
"""
import entity.user
from annotation.security import token_required
from entity.user import User
from exception.error_code import ErrorCode
from exception.field_exception import FieldException
from util import diff_match_patch as dmp_module

class DocumentService:

    def __init__(self):
        self.dmp = dmp_module.diff_match_patch()

    @token_required
    def apply_changes(self, current_user: entity.user.User, document_id: int, changes: str, is_patch: bool) -> bool:
        """
        Service method to apply the differential changes received for the document
        :param doc: The document id
        :param patch: The diff received for the document
        """

        access = self.check_document_access(current_user, document_id)
        if access is False:
            raise FieldException(code=ErrorCode.NO_AUTHORIZATION, message='User is not authorized to access this document')

        if is_patch:
            document_text = self.fetch_document_from_database(document_id)
            updated_text = self.apply_patch(document_text, changes)
        else:
            self.replace_document(document_id, changes)

        self.update_document_in_database(document_id, updated_text)

        return True

    @staticmethod
    def fetch_document_from_database(document_id: int):
        """
        Utility method to fetch document from database
        :param document_id: The document id
        :return: The text of the document fetched from the database
        """
        return ''

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

    @staticmethod
    def check_document_access(user: entity.user.User, document_id: int) -> bool:
        """
        Utility method to check document access for the logged in user
        :param user:
        :param document_id:
        :return:
        """
        return True

    def replace_document(self, document_id: int, changes: str) -> bool:
        """
        Utility method to update the document with the new content
        :param document_id:
        :param changes:
        :return:
        """
        return True