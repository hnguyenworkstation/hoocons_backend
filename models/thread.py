import mongoengine

from models.user import *
from models.thread_reply import BaseThreadReply


class BaseThread(Document):
    # Ownership and Managers
    created_by = ReferenceField('User', required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    title = StringField(required=True, min_length=10, max_length=150)
    text_content = StringField(required=True, min_length=10)
    images = ListField(StringField(), default=[])
    tags = ListField(StringField(), default=[])
    replies = ListField(ReferenceField(BaseThreadReply), default=[])
