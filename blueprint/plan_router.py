from typing import Dict, Any, List

from flask import Blueprint, request, jsonify

import entity.user
from annotation.security import token_required
from service.plan import PlanService
from service.document import DocumentService

plan = Blueprint('plan', __name__)

plan_service = PlanService()

@plan.route('/view/all', methods=['GET'])
#@token_required
#def view_all_plans(current_user: entity.user.User) -> List[Dict[Any, Any]]:
def view_all_plans() -> List[Dict[Any, Any]]:
    """
    Router method to view all applications created by user
    :param current_user: The logged in user
    :return: The application objects which are requested
    """
    plans = plan_service.viewAllPlans(None)
    return {'plans': plans}
