import mongoengine

from models.base_event import BaseEvent
from models.user import *


class BaseChannel(Document):
    # Ownership and Managers
    created_by = ReferenceField('User', required=True)
    owner = ReferenceField('User', default=created_by)
    moderators = ListField(ReferenceField('User'), default=[])

    # Channel information
    title = StringField(required=True)
    subtitle = StringField(required=True, unique=True)
    wallpaper_url = StringField(default=utils.get_random_wallpaper())
    profile_url = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow())
    location = PointField(default=[-179, -85])
    tags = ListField(StringField(), default=[])
    promote_image_urls = ListField(StringField())

    # Manage users in the channel
    followed_by = ListField(ReferenceField('User'), default=[])
    liked_by = ListField(ReferenceField('User'), default=[])
    reported_by = ListField(ReferenceField('User'), default=[])
    threads = ListField(ReferenceField('BaseThread'), default=[])

    meta = {'allow_inheritance': True}
