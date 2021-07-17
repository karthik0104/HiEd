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
from blueprint.university_router import university
from blueprint.user_rouer import user

app = Flask(__name__)
app.register_blueprint(university, url_prefix='/university')
app.register_blueprint(user, url_prefix='/user')

@app.route('/')
def default():
    return None

if __name__ == '__main__':
    app.run(host='localhost', port=5344)