from datetime import *
from mongoengine import *

import static.utils as utils

GENDER = ('Male', 'Female', 'Other')


class User(Document):
    username = StringField(unique=True, required=True, min_length=6)
    password = StringField(min_length=8, required=True)
    date_join = DateTimeField(default=datetime.utcnow())
    last_online = DateTimeField(default=datetime.utcnow())
    display_name = StringField()
    gender = StringField(max_length=6, choices=GENDER, default='Male')
    avatar = StringField(default=utils.get_default_avatar_url())
    birthday = DateTimeField()
    tokens = ListField(StringField(min_length=1))
    friends = ListField(ReferenceField('User'), default=[])
    friends_pending = ListField(ReferenceField('User'), default=[])
    friends_ignore = ListField(ReferenceField('User'), default=[])
    friends_request = ListField(ReferenceField('User'), default=[])
    timezone = StringField(default='UTC')
    location = GeoPointField(default=[-179, -85])

    def get_simple(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "gender": self.gender,
            "display_name": self.display_name,
            "avatar": self.avatar,
            "timezone": self.timezone,
            "location": self.location,
            "last_online": str(self.last_online)
        }

    def get_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "display_name": self.display_name,
            "gender": self.gender,
            "avatar": self.avatar,
            "timezone": self.timezone,
            "location": self.location,
            "last_online": str(self.last_online),
            "friends": [user.get_simple() for user in self.friends],
            "friends_pending": [user.get_simple() for user in self.friends_pending],
            "friends_request": [user.get_simple() for user in self.friends_request],
            "friends_ignore": [user.get_simple() for user in self.friends_ignore]
        }

    def __eq__(self, other):
        return self.username == other.username and self.password == other.password

    # default display la username
    def save(self, force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, signal_kwargs=None, **kwargs):
        if self.display_name is None or len(self.display_name) == 0:
            self.display_name = self.username[:len(self.username) - 2] + "**"
            print(self.display_name)
        return super(User, self).save()
