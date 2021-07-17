import json
from flask import Blueprint, jsonify
from service.university import UniversityService

university = Blueprint('university', __name__)

university_service = UniversityService()

@university.route('/view/<university_id>')
#@token_required
def view_university_details(university_id):
    university = university_service.getUniversityById(university_id)
    return university

