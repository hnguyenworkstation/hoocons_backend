import mongoengine

from models.user import *
from models.thread_reply import BaseThreadReply


class BaseThread(Document):
    """#################################################
        Field requirements:
            + created_by: user who created this thread
            + created_at: when was this thread created
            + title: thread title
            + text_content: content written among with the title
            + images: images attached
            + tags: those tags thing that user mention in the thread
            + replies: what people reply into this thread
            + is_blocked: is this thread blocked by admin (not allow to comment....)
            + is_pinned: is this thread pinned into a channel
    #################################################"""
    channel_owner = ReferenceField('BaseChannel', default="", required=True)
    created_by = ReferenceField('User', required=True)
    created_at = DateTimeField(default=datetime.utcnow())

    title = StringField(required=True, min_length=10, max_length=150)
    text_content = StringField(required=True, min_length=10)
    images = ListField(StringField(), default=[])
    tags = ListField(StringField(), default=[])

    replies = ListField(ReferenceField(BaseThreadReply), default=[])

    is_blocked = BooleanField(default=False)
    is_pinned = BooleanField(default=False)
