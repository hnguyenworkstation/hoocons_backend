import mongoengine

from models.user import *


class BaseThreadReply(Document):
    created_by = ReferenceField('User', required=True)
    text_content = StringField(default="", max_length=400)
    images = ListField(StringField(), default=[])
    is_edited = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow())
    liked_by = ListField(ReferenceField('User'), default=[])
    quoting = ReferenceField("BaseThreadReply", default="")
    quoted_by = ListField(ReferenceField("BaseThreadReply"), default=[])

    def get_content_json(self):
        quoting_jas = "" if self.quoting == "" else self.quoting.get_simple_json()
        return {
            "created_by": self.created_by.get_simple_header(),
            "text_content": self.text_content,
            "images": [image for image in self.images],
            "created_at": str(self.created_by),
            "quoting": quoting_jas,
            "is_edited": self.is_edited
        }

    def get_simple_json(self):
        return {
            "created_by": self.created_by.get_simple_header(),
            "text_content": self.text_content,
            "images": [image for image in self.images],
            "created_at": str(self.created_by)
        }
