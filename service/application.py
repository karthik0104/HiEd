from config.argsparser import ArgumentsParser
from entity.application import Application
from entity.university import University
from entity.course import Course
from entrypoint import db
from exception.field_exception import FieldException
from exception.error_code import ErrorCode

configs = ArgumentsParser()

class ApplicationService:

    def addApplication(self, current_user, data):
        university = db.session.query(University).filter_by(id=data['university_id']).first()
        if university is None:
            raise FieldException(code=ErrorCode.FIELD_ERROR, message='University field invalid')

        course = db.session.query(Course).filter_by(id=data['course_id']).first()
        if course is None:
            raise FieldException(code=ErrorCode.FIELD_ERROR, message='Course field invalid')

        application = Application(name=data['name'], university_id=university.id, course_id=course.id,
                                  year=data['year'], admit_term=data['admit_term'],
                                  area_of_specialization=data['area_of_specialization'], gre_score=data['gre_score'],
                                  toefl_ielts_score=data['toefl_ielts_score'], user=current_user)
        db.session.add(application)
        db.session.commit()
        return application

    def viewApplication(self, current_user, id):
        application = db.session.query(Application).filter_by(id=id).first()
        #return application._asdict()
        return application