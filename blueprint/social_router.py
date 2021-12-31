from typing import Dict, Any, List

from flask import Blueprint, request, jsonify

import entity.user
from annotation.security import token_required
from service.social import SocialService

social = Blueprint('social', __name__)

social_service = SocialService()

@social.route('/discussion-threads/<group_id>', methods=['GET'])
#@token_required
#def view_all_discussion_threads_by_group(current_user: entity.user.User) -> List[Dict[Any, Any]]:
def view_all_discussion_threads_by_group(group_id) -> List[Dict[Any, Any]]:
    discussion_threads = social_service.getDiscussionThreadsByGroup(None, group_id)
    return {'discussion_threads': discussion_threads}


@social.route('/discussion-group/create', methods=['POST'])
#@token_required
#def view_all_discussion_threads_by_group(current_user: entity.user.User) -> List[Dict[Any, Any]]:
def create_discussion_group() -> List[Dict[Any, Any]]:
    data = request.get_json()
    discussion_group = social_service.createDiscussionGroup(None, data)
    return jsonify(discussion_group)


@social.route('/discussion-group/view/all', methods=['GET'])
#@token_required
#def view_all_discussion_threads_by_group(current_user: entity.user.User) -> List[Dict[Any, Any]]:
def get_discussion_groups() -> List[Dict[Any, Any]]:
    page_number = request.args['page_number']

    discussion_groups = social_service.getDiscussionGroups(None, page_number)
    print(discussion_groups)
    return {'discussion_groups': discussion_groups}
