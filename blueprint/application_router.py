from flask import Blueprint, request, jsonify

from security.annotation import token_required
from service.application import ApplicationService

application = Blueprint('application', __name__)

application_service = ApplicationService()

@application.route('/create', methods=['POST'])
@token_required
def add_application(current_user):
    data = request.get_json()
    application = application_service.addApplication(current_user, data)
    return jsonify(application)

@application.route('/view/<id>', methods=['GET'])
@token_required
def view_application(current_user, id):
    application = application_service.viewApplication(current_user, id)
    print(application)
    print(jsonify(application))
    return jsonify(application)
