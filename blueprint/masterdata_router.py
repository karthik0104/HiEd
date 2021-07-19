from flask import Blueprint, request, jsonify

from security.annotation import token_required
from service.masterdata import MasterdataService

mdm = Blueprint('mdm', __name__)

mdm_service = MasterdataService()

@mdm.route('/bulk-import', methods=['POST'])
@token_required
def bulk_import(current_user):
    status = mdm_service.update_masterdata(current_user)
    return status