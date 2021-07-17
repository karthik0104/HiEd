from flask import Blueprint
from service.university import UniversityService

university = Blueprint('university', __name__)

university_service = UniversityService()

@university.route('/view/<university-id>')
def view_university_details(university_id):
    university_service.getUniversityById(university_id)
    return None

