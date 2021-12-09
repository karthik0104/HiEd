from typing import Dict, Any, List

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

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
#@token_required
#def view_all_universities_lite(current_user: entity.user.User) -> List[Dict[Any, Any]]:
def view_all_universities_lite() -> List[Dict[Any, Any]]:
    """

    :param current_user:
    :return:
    """
    all_universities = university_service.getAllUniversityCourses(None, lite=True, query=request.args['q'])
    return all_universities

@university.route('/search')
@cross_origin()
#@token_required
#def search_universities(current_user: entity.user.User) -> Dict[Any, Any]:
def search_universities() -> Dict[Any, Any]:
    """

    :param current_user:
    :return:
    """
    universities = university_service.getUniversitiesBySearchQuery(None, request.args['q'])
    return {'universities': universities}

@university.route('/course-deadline', methods=['POST'])
@cross_origin()
#@token_required
#def get_course_deadline(current_user: entity.user.User) -> Dict[Any, Any]:
def get_course_deadline() -> Dict[Any, Any]:
    """

    :param current_user:
    :return:
    """
    data = request.get_json()
    course_deadline = university_service.getCourseDeadline(None, data)
    return {'course_deadline': course_deadline}
