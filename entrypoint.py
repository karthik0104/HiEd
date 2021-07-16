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
'''

from flask import Flask
from blueprint.university_router import university

app = Flask(__name__)
app.register_blueprint(university)

@app.route('/')
def default():
    return None