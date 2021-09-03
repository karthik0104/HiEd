from typing import Dict, Any

from flask import Blueprint, request, jsonify

import entity.user
from annotation.security import token_required
from service.application import ApplicationService

application = Blueprint('application', __name__)

application_service = ApplicationService()

@application.route('/create', methods=['POST'])
@token_required
def add_application(current_user: entity.user.User) -> Dict[Any, Any]:
    """
    Router method to add the application
    :param current_user: The logged in user
    :return: The application object which is added into the system
    """
    data = request.get_json()
    application = application_service.addApplication(current_user, data)
    return jsonify(application)

@application.route('/view/<id>', methods=['GET'])
@token_required
def view_application(current_user: entity.user.User, id: int) -> Dict[Any, Any]:
    """
    Router method to view an application
    :param current_user: The logged in user
    :param id: The application id which is required
    :return: The application object which is requested
    """
    application = application_service.viewApplication(current_user, id)
    print(application)
    print(jsonify(application))
    return jsonify(application)
