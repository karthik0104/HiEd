from typing import Dict, Any, List

from flask import Blueprint, request, jsonify

import entity.user
from annotation.security import token_required
from service.university import UniversityService

university = Blueprint('university', __name__)

university_service = UniversityService()

@university.route('/view/<university_id>')
@token_required
def view_university_details(current_user: entity.user.User, university_id: int) -> Dict[Any, Any]:
    """

    :param current_user:
    :param university_id:
    :return:
    """
    university = university_service.getUniversityById(current_user, university_id)
    return university

@university.route('/view/courses')
@token_required
def view_all_universities_lite(current_user: entity.user.User) -> List[Dict[Any, Any]]:
    """

    :param current_user:
    :return:
    """
    all_universities = university_service.getAllUniversityCourses(current_user, lite=True)
    return all_universities

@university.route('/search')
@token_required
def search_universities(current_user: entity.user.User) -> Dict[Any, Any]:
    """

    :param current_user:
    :return:
    """
    universities = university_service.getUniversitiesBySearchQuery(current_user, request.args['q'])
    return {'universities': universities}
