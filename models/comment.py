from datetime import *

import mongoengine
from static import app_constant

from mongoengine import *


class BaseComment(Document):
    # Created with base data
    create_by = ReferenceField('User', required=True)
    text_context = StringField(default="")
    image = StringField(default="")
    create_at = DateTimeField(default=datetime.utcnow())
    reply_to = StringField(default="")

    def get_reply_comment(self):
        comment = BaseComment.objects(id=self.reply_to).first()
        if comment is None:
            return None
        else:
            return {
                "created_by": comment.created_by.get_simple_header(),
                "text_context": comment.text_context,
                "image": comment.image
            }

    def get_complete_json(self):
        if self.reply_to is None or len(self.reply_to) == 0:
            return {
                "created_by": self.created_by.get_simple_header(),
                "text_context": self.text_context,
                "image": self.image,
                "create_at": self.create_at
            }
        else:
            return {
                "created_by": self.created_by.get_simple_header(),
                "text_context": self.text_context,
                "image": self.image,
                "create_at": self.create_at,
                "reply_to": self.get_reply_comment()
            }
