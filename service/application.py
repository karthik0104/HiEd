import entity.user
from annotation.serializer import serialize_db_result
from config.argsparser import ArgumentsParser
from entity.application import Application
from entity.plan import Plan
from entity.university import University
from entity.course import Course
from entrypoint import db
from exception.field_exception import FieldException
from exception.error_code import ErrorCode
from typing import Dict, Any, List
import dateutil.parser

configs = ArgumentsParser()

class ApplicationService:

    def addApplication(self, current_user: entity.user.User, data: Dict[Any, Any]) -> entity.application.Application:
        """
        Service method for adding an application into the system
        :param current_user: The logged in user
        :param data: The application request received from the frontend
        :return: Application object which is added into the system
        """
        _university = db.session.query(University).filter_by(name=data['university']).first()
        if _university is None:
            raise FieldException(code=ErrorCode.FIELD_ERROR, message='University field invalid')

        _course = db.session.query(Course).filter_by(name=data['course']).first()
        if _course is None:
            raise FieldException(code=ErrorCode.FIELD_ERROR, message='Course field invalid')

        _application = Application(name=data['name'], university_id=_university.id, course_id=_course.id,
                                  year=data['year'], admit_term=data['admit_term'],
                                  area_of_specialization=data['area_of_specialization'], gre_score=data['gre_score'],
                                  toefl_ielts_score=data['toefl_ielts_score'], user=current_user)


        try:
            db.session.add(_application)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

        try:
            start_date = dateutil.parser.isoparse(data['start_date'])
            end_date = dateutil.parser.isoparse(data['end_date'])

            _plan = Plan(application_id=_application.id, plan_stage_id=1, start_date=start_date.strftime('%Y-%m-%d'),
                         end_date=end_date.strftime('%Y-%m-%d'))

            db.session.add(_plan)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

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

    @serialize_db_result
    def viewAllApplications(self, current_user: entity.user.User) -> List[entity.application.Application]:
        """
        Service method for viewing all applications created by the user
        :param current_user: The logged in user
        :return: List of application objects which are requested
        """
        #_applications = db.session.query(Application.id.label('id'), Application.name.label('name')).\
        #    filter_by(user_id=current_user.id).all()
        _applications = db.session.query(Application.id.label('id'), Application.name.label('name')).all()
        return _applications