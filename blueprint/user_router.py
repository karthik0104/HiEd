from flask import Blueprint, request, jsonify
from service.user import UserService

user = Blueprint('user', __name__)

user_service = UserService()

@user.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()
    user = user_service.register_user(data)

    return jsonify(user)

@user.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization
    token = user_service.login_user(auth)

    return token