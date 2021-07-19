from flask import Blueprint

from security.annotation import token_required
from service.university import UniversityService

university = Blueprint('university', __name__)

university_service = UniversityService()

@university.route('/view/<university_id>')
@token_required
def view_university_details(current_user, university_id):
    university = university_service.getUniversityById(current_user, university_id)
    return university

