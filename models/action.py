from datetime import datetime

from mongoengine import *

from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource
from models.user import User

from static import app_constant


class BaseAction(Document):
    """
        @by_user: Who makes this action
        @action_type = LIKE, SHARE, MAKING FRIENDS, POST EVENT ....
        @target: Id of target (event, user)
        @with_content: Maybe NONE since content only available for comment
    """
    by_user = ReferenceField('User', required=True)
    action_type = StringField(default="", choices=app_constant.ACTION_TYPES)
    target = StringField(default="")
    with_content = StringField(default="")

    def get_complete_json(self):
        return {
            "id": self.id,
            "by_user": self.by_user.get_simple_header(),
            "target": self.target.get_complete_json(),
            "with_content": self.get_complete_json()
        }
