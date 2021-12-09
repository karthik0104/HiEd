from flask import Blueprint, request, jsonify

from annotation.security import token_required
from service.metadata import MetadataService

metadata = Blueprint('metadata', __name__)

metadata_service = MetadataService()

@metadata.route('/ui-metadata', methods=['GET'])
#@token_required
#def get_metadata(current_user):
def get_metadata():
    response = metadata_service.get_metadata(None)
    return jsonify(response)

@metadata.route('/create-plan', methods=['GET'])
#@token_required
#def get_metadata(current_user):
def get_create_plan_metadata():
    response = metadata_service.get_create_plan_metadata(None)
    return jsonify(response)