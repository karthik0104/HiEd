'''
The main Flask entrypoint script which contains all the APIs and Blueprint definitions for the application.
'''

'''
List of Entities:
1. University
2. Applicant
3. User
4. Application
5. Document

The primary util system which we will be using for storage is MySQL. We will also be using MongoDB for Document storage.

SQLAlchemy would be used as an ORM solution.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

        app.register_blueprint(university, url_prefix='/university')
        app.register_blueprint(user, url_prefix='/user')
        app.register_blueprint(application, url_prefix='/application')
        app.register_blueprint(mdm, url_prefix='/masterdata')

        #db.create_all()  # Create sql tables for our data models

        return app

if __name__ == '__main__':
    app = init_app()
    app.run(host='localhost', port=5344)