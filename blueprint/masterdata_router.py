from flask import Blueprint, request, jsonify

from security.annotation import token_required
from service.masterdata import MasterdataService

mdm = Blueprint('mdm', __name__)

mdm_service = MasterdataService()

@mdm.route('/bulk-university-import', methods=['POST'])
@token_required
def bulk_university_import(current_user):
    status = mdm_service.update_masterdata()
    return status

@mdm.route('/locale-bundle-import', methods=['POST'])
@token_required
def bulk_locale_import(current_user):
    status = mdm_service.update_locale_data()
    return status