from config.argsparser import ArgumentsParser
from entity.university import University
from entity.course import Course
from entrypoint import db

configs = ArgumentsParser()

class UniversityService:
    #session = DataConnector.getSession(configs.db_host, configs.db_user, configs.db_password, configs.db_database)

    def addUniversity(self, current_user, data):
        university = University(data['name'])
        db.session.add(university)
        db.session.commit()
        return university

    def getUniversityById(self, current_user, id):
        our_univ = db.session.query(University.name.label('name')).filter_by(id=id).first()
        return our_univ._asdict()

    def getAllUniversityCourses(self, current_user, lite=False):
        #all_courses = db.session.query(Course.name.label('name'), University.name.label('university_name')).all()
        all_courses = db.session.query(Course.name.label('name'),
                                       University.name.label('university_name'))\
            .join(University).filter_by(name='Syracuse University').all()
        result = []

        for course in all_courses:
            u = course._asdict()
            result.append(u)

        return {'courses': result}