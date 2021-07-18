import datetime
import uuid

import jwt
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from config.argsparser import ArgumentsParser
from entity.user import User
from entrypoint import db

configs = ArgumentsParser()

class UserService:
    #session = DataConnector.getSession(configs.db_host, configs.db_user, configs.db_password, configs.db_database)

    def register_user(self, data):
        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        return new_user

    def login_user(self, auth):

        if not auth or not auth.username or not auth.password:
            return 'Invalid'

        user = db.session.query(User).filter_by(name=auth.username).first()

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow()
                                            + datetime.timedelta(days=configs.token_validity_in_days)}, configs.secret_key)
            return jsonify({'token': token.decode('UTF-8')})

        return 'Invalid'