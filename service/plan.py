import entity.user
from annotation.serializer import convert_db_row_to_dict
from config.argsparser import ArgumentsParser
from entity.application import Application
from entity.plan import Plan, PlanStageMasterdata
from entity.university import University
from entity.course import Course
from entrypoint import db
from exception.field_exception import FieldException
from exception.error_code import ErrorCode
from typing import Dict, Any, List
import dateutil.parser

configs = ArgumentsParser()

class PlanService:

    @convert_db_row_to_dict
    def viewAllPlans(self, current_user: entity.user.User) -> List[entity.application.Application]:
        """
        Service method for viewing all applications created by the user
        :param current_user: The logged in user
        :return: List of application objects which are requested
        """
        #_applications = db.session.query(Application.id.label('id'), Application.name.label('name')).\
        #    filter_by(user_id=current_user.id).all()
        _plans = db.session.query(Application.id.label('id'), Application.name.label('name'),
                                         Plan.start_date.label('start_date'), Plan.end_date.label('end_date'),
                                         PlanStageMasterdata.name.label('plan_stage'))\
            .join(Plan, Plan.application_id == Application.id).join(PlanStageMasterdata, PlanStageMasterdata.id == Plan.plan_stage_id).all()
        return _plans