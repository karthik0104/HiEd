from flask import Blueprint, request, jsonify

from security.annotation import token_required
from service.metadata import MetadataService

metadata = Blueprint('metadata', __name__)

metadata_service = MetadataService()

@metadata.route('/all', methods=['POST'])
@token_required
def get_metadata(current_user):
    status = metadata_service.get_metadata()
    return status