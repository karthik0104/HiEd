from flask import Blueprint, request, jsonify

from annotation.security import token_required
from service.university import UniversityService

university = Blueprint('university', __name__)

university_service = UniversityService()

@university.route('/view/<university_id>')
@token_required
def view_university_details(current_user, university_id):
    university = university_service.getUniversityById(current_user, university_id)
    return university

@university.route('/view/courses')
@token_required
def view_all_universities_lite(current_user):
    all_universities = university_service.getAllUniversityCourses(current_user, lite=True)
    return all_universities

@university.route('/search')
@token_required
def search_universities(current_user):
    universities = university_service.getUniversitiesBySearchQuery(current_user, request.args['q'])
    return {'universities': universities}
