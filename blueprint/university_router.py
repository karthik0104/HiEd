from flask import Blueprint

university = Blueprint('university', __name__)

@university.route('/view')
def view_university_details():
    return None

