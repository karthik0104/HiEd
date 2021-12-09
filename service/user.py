import datetime
import uuid

import jwt
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from config.argsparser import ArgumentsParser
from entity.user import User
from entity.locale import Locale
from entrypoint import db
from exception.error_code import ErrorCode
from exception.field_exception import FieldException
from util.mongodb import MongoConnection

configs = ArgumentsParser()

class UserService:
    #session = DataConnector.getSession(configs.db_host, configs.db_user, configs.db_password, configs.db_database)

    MIN_LATITUDE = -90
    MAX_LATITUDE = 90
    MIN_LONGITUDE = -180
    MAX_LONGITUDE = 180

    GEOLOCATION_COLLECTION = 'user-geolocation'

    default_user_locale = 'EN'

    def register_user(self, data):
        hashed_password = generate_password_hash(data['password'], method='sha256')

        if ('locale' not in data) or (data['locale'] is None):
            data['locale'] = self.default_user_locale

        locale = db.session.query(Locale).filter_by(language=data['locale']).first()
        if locale is None:
            return None

        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, locale_id=locale.id)

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
            return jsonify({'token': token.decode('UTF-8'), 'locale': user.locale.language})

        return 'Invalid'


    def save_user_location(self, user, data):
        """
        Service method to save the user location in form of coordinates
        :param data: The latitude and longitude of the the user
        :return:
        """
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])

        # Validate co-ordinates
        if (self.MIN_LONGITUDE <= longitude <= self.MAX_LONGITUDE) and (self.MIN_LATITUDE <= latitude <= self.MAX_LATITUDE):
            pass
        else:
            raise FieldException(code=ErrorCode.INVALID_COORDINATES, message='The co-ordinates specified are invalid')

        self.persist_user_location(user, latitude, longitude)

        return None

    def persist_user_location(self, user, latitude, longitude):
        """
        Utility method to persist the user's geo coordinates in the database
        :param user: The logged in user
        :param latitude: The latitude
        :param longitude: The longitude
        :return:
        """
        mongo_connection = MongoConnection(configs.mongo_username, configs.mongo_password, configs.mongo_server,
                                                configs.mongo_database)
        mongo_connection.connect()

        try:
            geolocation_collection = mongo_connection.get_collection(self.GEOLOCATION_COLLECTION)
            mongo_connection.persist_geolocation(collection=geolocation_collection, user_id=user.id, latitude=latitude, longitude=longitude)
        finally:
            mongo_connection.close()

        return None

    def find_closest_locations(self, user):
        """
        Service method to return closest locations to specified location
        :param user:
        :return:
        """
        mongo_connection = MongoConnection(configs.mongo_username, configs.mongo_password, configs.mongo_server,
                                                configs.mongo_database)
        mongo_connection.connect()

        geolocation_closest_points = []

        try:
            geolocation_collection = mongo_connection.get_collection(self.GEOLOCATION_COLLECTION)
            geolocation_document = mongo_connection.find_by_fields(geolocation_collection, {"user_id": user.id}, multiple=False)
            geolocation_closest_points = mongo_connection.find_closest_points(geolocation_collection,
                                                 geolocation_document['location']['coordinates'][0],
                                                 geolocation_document['location']['coordinates'][1])
        finally:
            mongo_connection.close()

        return geolocation_closest_points