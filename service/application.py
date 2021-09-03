import entity.user
from config.argsparser import ArgumentsParser
from entity.application import Application
from entity.university import University
from entity.course import Course
from entrypoint import db
from exception.field_exception import FieldException
from exception.error_code import ErrorCode
from typing import Dict, Any

configs = ArgumentsParser()

class ApplicationService:

    def addApplication(self, current_user: entity.user.User, data: Dict[Any, Any]) -> entity.application.Application:
        """
        Service method for adding an application into the system
        :param current_user: The logged in user
        :param data: The application request received from the frontend
        :return: Application object which is added into the system
        """
        _university = db.session.query(University).filter_by(id=data['university_id']).first()
        if _university is None:
            raise FieldException(code=ErrorCode.FIELD_ERROR, message='University field invalid')

        _course = db.session.query(Course).filter_by(id=data['course_id']).first()
        if _course is None:
            raise FieldException(code=ErrorCode.FIELD_ERROR, message='Course field invalid')

        _application = Application(name=data['name'], university_id=_university.id, course_id=_course.id,
                                  year=data['year'], admit_term=data['admit_term'],
                                  area_of_specialization=data['area_of_specialization'], gre_score=data['gre_score'],
                                  toefl_ielts_score=data['toefl_ielts_score'], user=current_user)
        db.session.add(_application)
        db.session.commit()
        return _application

    def viewApplication(self, current_user: entity.user.User, application_id: int) -> entity.application.Application:
        """
        Service method for viewing an application
        :param current_user: The logged in user
        :param id: The application id which is requested
        :return: The application object which is requested
        """
        _application = db.session.query(Application).filter_by(id=application_id).first()

        # Add resource authorization check
        if _application.user_id != current_user.id:
            raise FieldException(code=ErrorCode.NO_AUTHORIZATION, message='Not authorized to access the requested resource')

        #return application._asdict()
        return _application