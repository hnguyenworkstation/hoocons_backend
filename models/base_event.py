from datetime import *

import mongoengine
from static import app_constant

from mongoengine import *


class BaseEvent(Document):
    # Created with base data
    create_by = ReferenceField('User')
    text_context = StringField(default="")
    link_avatar = ListField(default=[])
    contain_event = ReferenceField('BaseEvent')
    create_at = DateTimeField(default=datetime.utcnow())
    privacy = StringField(choices=app_constant.ACCESS, default='Friend')
    comments = ListField(ReferenceField('Comment'), default=[], reverse_delete_rule=mongoengine.PULL)

    # Like - Comment - Share - Report
    reported_by = ListField(ReferenceField('User'), default=[])
    liked_by = ListField(ReferenceField('User'), default=[])
    shared_by = ListField(ReferenceField('User'), default=[])
    tags = ListField(StringField(max_length=20), default=[])

    location = PointField(default=[-179, -85])
    active_time = DateTimeField(default=datetime.utcnow())
    meta = {'allow_inheritance': True}

