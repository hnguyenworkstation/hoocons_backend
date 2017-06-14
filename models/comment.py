from datetime import *

import mongoengine
from static import app_constant

from mongoengine import *


class BaseReplyComment(EmbeddedDocument):
    # Created with base data
    create_by = ReferenceField('User', required=True)
    text_content = StringField(default="")
    image = StringField(default="")
    create_at = DateTimeField(default=datetime.utcnow())
    liked_by = ListField(ReferenceField('User'), default=[])
    is_edited = BooleanField(default=False)

    def get_complete_json(self):
        return {
            "created_by": self.created_by.get_simple_header(),
            "create_at": self.create_at,
            "text_content": self.text_content,
            "image": self.image,
            "likes_count": len(self.liked_by),
            "is_edited": self.is_edited
        }


class BaseComment(EmbeddedDocument):
    # Created with base data
    create_by = ReferenceField('User', required=True)
    text_content = StringField(default="")
    image = StringField(default="")
    create_at = DateTimeField(default=datetime.utcnow())
    liked_by = ListField(ReferenceField('User'), default=[])
    is_edited = BooleanField(default=False)
    replies = ListField(EmbeddedDocumentField(BaseReplyComment), default=[])

    def get_complete_json(self):
        return {
            "created_by": self.created_by.get_simple_header(),
            "create_at": self.create_at,
            "text_content": self.text_content,
            "image": self.image,
            "likes_count": len(self.liked_by),
            "is_edited": self.is_edited,
            "replies": len(self.replies)
        }


