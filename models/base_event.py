from datetime import *

import mongoengine
from mongoengine import *

from static import app_constant


class BaseEvent(Document):
    # Created with base data
    create_by = ReferenceField('User', required=True)
    text_context = StringField(default="")
    images = ListField(default=[])
    contain_event = StringField(default=[])
    create_at = DateTimeField(default=datetime.utcnow())
    privacy = StringField(choices=app_constant.ACCESS, default='Friend')
    comments = ListField(ReferenceField('BaseComment'), default=[], reverse_delete_rule=mongoengine.PULL)

    # Like - Comment - Share - Report
    reported_by = ListField(ReferenceField('User'), default=[])
    liked_by = ListField(ReferenceField('User'), default=[])
    shared_by = ListField(ReferenceField('User'), default=[])
    tags = ListField(StringField(max_length=20), default=[])

    location = GeoPointField(default=[-179, -85])
    active_time = DateTimeField(default=datetime.utcnow())
    meta = {'allow_inheritance': True}

    def get_shared_event_json(self):
        event = BaseEvent.objects(id=self.contain_event).first()
        if event is None:
            return ""
        else:
            return {
                "id": str(self.event.id),
                "create_by": self.event.create_by.get_simple_header(),
                "text_context": self.event.text_context,
                "images": [image for image in self.event.images],
            }

    def get_initial_json(self):
        if self.contain_event is None or len(self.contain_event) < 12:
            return {
                "id": str(self.id),
                "create_by": self.create_by.get_simple_header(),
                "create_at": str(self.create_at),
                "text_context": self.text_context,
                "images": [image for image in self.images],
                "contain_event": ""
            }
        else:
            return {
                "id": str(self.id),
                "create_by": self.create_by.get_simple_header(),
                "create_at": str(self.create_at),
                "text_context": self.text_context,
                "images": [image for image in self.images],
                "contain_event": self.get_shared_event_json()
            }

    def get_complete_json(self):
        like_count = len(self.liked_by)
        report_count = len(self.reported_by)
        comment_count = len(self.comments)
        if self.contain_event is None or len(self.contain_event) < 12:
            return {
                "id": str(self.id),
                "create_by": self.create_by.get_simple_header(),
                "create_at": str(self.create_at),
                "text_context": self.text_context,
                "images": [image for image in self.images],
                "contain_event": "",
                "like_count": like_count,
                "comment_count": comment_count,
                "report_count": report_count
            }
        else:
            return {
                "id": str(self.id),
                "create_by": self.create_by.get_simple_header(),
                "create_at": str(self.create_at),
                "text_context": self.text_context,
                "images": [image for image in self.images],
                "contain_event": self.get_shared_event_json(),
                "like_count": like_count,
                "comment_count": comment_count,
                "report_count": report_count
            }

