import jwt
from functools import wraps
from flask import request, jsonify
from entity.user import User
from config.argsparser import ArgumentsParser

configs = ArgumentsParser()

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'A valid token is missing'})
        try:
            data = jwt.decode(token, configs.secret_key)
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator