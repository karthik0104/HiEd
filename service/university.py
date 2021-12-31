from config.argsparser import ArgumentsParser
from entity.university import University
from entity.course import Course
from entrypoint import db
from sqlalchemy import func
from annotation.serializer import serialize_db_result
from util.serializer import alchemy_encoder
import json

configs = ArgumentsParser()

class UniversityService:
    #session = DataConnector.getSession(configs.db_host, configs.db_user, configs.db_password, configs.db_database)

    def addUniversity(self, current_user, data):
        university = University(data['name'])
        db.session.add(university)
        db.session.commit()
        return university

    def getUniversityById(self, current_user, id):
        #our_univ = db.session.query(University.name.label('name')).filter_by(id=id).first()
        # return our_univ._asdict()
        our_univ = db.session.query(University).filter_by(id=id).first()
        return json.dumps(our_univ, cls=alchemy_encoder(), check_circular=False)

    def getAllUniversityCourses(self, current_user, lite=False, query=''):
        #all_courses = db.session.query(Course.name.label('name'), University.name.label('university_name')).all()
        all_courses = db.session.query(Course.name.label('name'),
                                       University.name.label('university_name'))\
            .join(University).filter_by(name=query).all()
        result = []

        for course in all_courses:
            u = course._asdict()
            result.append(u)

        return {'courses': result}

    @serialize_db_result
    def getUniversitiesBySearchQuery(self, current_user, query):
        search_query = "%{}%".format(query)
        universities = db.session.query(University.id.label('id'), University.name.label('name')).\
            filter(func.lower(University.name).like(func.lower(search_query))).all()

        return universities

    def getCourseDeadline(self, current_user, data):
        university = db.session.query(University).filter_by(name=data['university']).first()
        course = db.session.query(Course).filter(Course.name==data['course'], Course.university_id==university.id).first()
        course_deadlines = json.loads(course.deadline)

        return course_deadlines[data['admit_term']]
