from typing import Dict, Any, List

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from annotation.security import token_required
from service.document import DocumentService

document = Blueprint('document', __name__)
document_service = DocumentService()

@document.route('/upload-data', methods=['POST'])
@cross_origin()
def upload_data():
    """
    Router method to enable file upload and saving onto the storage system
    :return: status indicating whether upload was successful or not
    """
    file = request.files['file']
    status = document_service.upload_data(None, file)

    return {"status": status}

@document.route('/create-document', methods=['POST'])
@cross_origin()
def create_document():
    """
    Router method to perform document creation and storage on the database system
    :return: result containing the document ID
    """
    data = request.get_json()
    result = document_service.create_document(None, document_exists=True, file_name=data['file_name'])

    return result

@document.route('/view/all', methods=['GET'])
@cross_origin()
def view_all_documents():
    """
    Router method to fetch all documents created by the user
    :return: list of documents created by the user
    """
    result = document_service.fetch_all_user_documents(None)

    return result