from functools import wraps

import jwt
from flask import request, jsonify

from config.argsparser import ArgumentsParser
from entity.user import User
from entrypoint import db

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
            current_user = db.session.query(User).filter_by(public_id=data['public_id']).first()
        except:
           return jsonify({'message': 'Token is invalid'})

        if not current_user:
            return jsonify({'message': 'A valid token is missing'})

        return f(current_user, *args, **kwargs)
    return decorator