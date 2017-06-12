from datetime import datetime

from mongoengine import *

from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource
from models.user import User


class BaseAction(Document):
    """
        @by_user: Who makes this action
        @action_type = LIKE, SHARE, MAKING FRIENDS, POST EVENT ....
        @target: Id of target (event, user)
        @with_content: Maybe NONE since content only available for comment
    """
    by_user = ReferenceField('User', required=True)
    action_type = StringField(default="")
    target = StringField(default="")
    with_content = StringField(default="")

    def get_complete_json(self):
