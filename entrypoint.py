'''
The main Flask entrypoint script which contains all the APIs and Blueprint definitions for the application.
'''
from exception.error_code import ErrorCode

'''
List of Entities:
1. University
2. Applicant
3. User
4. Application
5. Document
6. Course
7. Locale & LocaleField

The primary util system which we will be using for storage is MySQL. We will also be using MongoDB for Document storage and User Location storage.
SQLAlchemy would be used as an ORM solution.

The application also uses Web Sockets to handle faster and real-time communication with multiple clients.
'''

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send

db = SQLAlchemy()

def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('app_config.Config')

    db.init_app(app)

    with app.app_context():
        from blueprint.university_router import university
        from blueprint.user_router import user
        from blueprint.application_router import application
        from blueprint.masterdata_router import mdm
        from blueprint.metadata_router import metadata

        app.register_blueprint(university, url_prefix='/university')
        app.register_blueprint(user, url_prefix='/user')
        app.register_blueprint(application, url_prefix='/application')
        app.register_blueprint(mdm, url_prefix='/masterdata')
        app.register_blueprint(metadata, url_prefix='/metadata')

        #db.create_all()  # Create sql tables for our data models

        @app.route('/')
        def index():
            return render_template('index.html')


        #@app.errorhandler(Exception)
        def handle_error(error):
            response = {}
            response['error_type'] = type(error).__name__

            if hasattr(error, 'code'):
                response['error_code'] = error.code.value
            else:
                response['error_code'] = ErrorCode.GENERIC_ERROR.value

            if hasattr(error, 'message'):
                response['message'] = error.message
            else:
                response['message'] = 'Generic Error'
            return response

        return app


if __name__ == '__main__':
    app = init_app()

    socketIo = SocketIO(app, cors_allowed_origins="*")

    #from service.message_handler import connectUser, handleSocketMessage, disconnectUser

    @socketIo.on("connect")
    def connect():
        print('Connected')
        print(request.sid)
        #connectUser(request.sid)

    @socketIo.on("message")
    def handleMessage(msg):
        print(msg)
        print(request.sid)
        #handleSocketMessage(msg, request.sid)
        send("Message from server !", room=['dummy_id', request.sid])

    @socketIo.on("disconnect")
    def disconnect():
        print('Disconnected')
        print(request.sid)
        #disconnectUser(request.sid)

    print('Branch change test !')
    socketIo.run(app, host='localhost', port=5344)
    #app.run(host='localhost', port=5344)
