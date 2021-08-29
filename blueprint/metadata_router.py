from flask import Blueprint, request, jsonify

from annotation.security import token_required
from service.metadata import MetadataService

metadata = Blueprint('metadata', __name__)

metadata_service = MetadataService()

@metadata.route('/ui-metadata', methods=['GET'])
@token_required
def get_metadata(current_user):
    response = metadata_service.get_metadata(current_user)
    return jsonify(response)