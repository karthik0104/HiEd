from functools import wraps

import jwt
from flask import request, jsonify

from config.argsparser import ArgumentsParser
from entity.user import User
from entrypoint import db
from exception.error_code import ErrorCode
from exception.field_exception import FieldException

configs = ArgumentsParser()

def token_required(f: object) -> object:
    """

    :param f: 
    :return:
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        _token = None

        if 'x-access-tokens' in request.headers:
            _token = request.headers['x-access-tokens']

        if not _token:
            raise FieldException(code=ErrorCode.TOKEN_MISSING, message='A valid token is missing')
        try:
            data = jwt.decode(_token, configs.secret_key)
            _current_user = db.session.query(User).filter_by(public_id=data['public_id']).first()
        except:
           raise FieldException(code=ErrorCode.TOKEN_INVALID, message='A valid token is missing')

        if not _current_user:
            raise FieldException(code=ErrorCode.TOKEN_MISSING, message='A valid token is missing')

        return f(_current_user, *args, **kwargs)
    return decorator