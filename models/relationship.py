from datetime import *
from mongoengine import *
from database import mlab

from static import utils, app_constant


class Relationship(Document):
    between_users = ListField(required=True)
    date_of_action = DateTimeField(default=datetime.utcnow())
    status = StringField(choices=app_constant.FRIEND_STATUS, max_length=10)

    def get_json(self):
        return mlab.item2json(self)

    def get_date_of_action(self):
        return self.date_of_action

    def get_status(self):
        return self.status

