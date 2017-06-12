from datetime import *

import mongoengine
from static import app_constant

from mongoengine import *


class BaseComment(Document):
    # Created with base data
    create_by = ReferenceField('User', required=True)
    text_content = StringField(default="")
    image = StringField(default="")
    create_at = DateTimeField(default=datetime.utcnow())
    liked_by = ListField(ReferenceField('User'), default=[])
    reply_to = StringField(default="")
    is_edited = BooleanField(default=False)

    def get_reply_comment(self):
        comment = BaseComment.objects(id=self.reply_to).first()
        if comment is None:
            return None
        else:
            return {
                "created_by": comment.created_by.get_simple_header(),
                "text_content": comment.text_content,
                "image": comment.image
            }

    def get_complete_json(self):
        if self.reply_to is None or len(self.reply_to) == 0:
            return {
                "created_by": self.created_by.get_simple_header(),
                "text_content": self.text_content,
                "likes_count": len(self.liked_by),
                "image": self.image,
                "create_at": self.create_at
            }
        else:
            return {
                "created_by": self.created_by.get_simple_header(),
                "create_at": self.create_at,
                "text_content": self.text_content,
                "image": self.image,
                "reply_to": self.get_reply_comment(),
                "likes_count": len(self.liked_by)
            }
