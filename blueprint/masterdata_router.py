from flask import Blueprint, request, jsonify

from annotation.security import token_required
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

@mdm.route('/plan-stages-metadata-import', methods=['POST'])
@token_required
def plan_stages_metadata_import(current_user):
    status = mdm_service.update_plan_masterdata()
    return status