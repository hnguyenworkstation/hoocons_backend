from datetime import *
from mongoengine import *

from static import utils, app_constant
from models.relationship import Relationship


class User(Document):
    username = StringField(unique=True, required=True, min_length=6)
    password = StringField(min_length=8, required=True)
    display_name = StringField()
    nickname = StringField()
    date_join = DateTimeField(default=datetime.utcnow())
    last_online = DateTimeField(default=datetime.utcnow())
    gender = StringField(max_length=6, choices=app_constant.GENDER, default='Male')
    profile_url = StringField(default=utils.get_default_avatar_url())
    birthday = DateTimeField()
    location = GeoPointField(default=[-179, -85])
    is_sharing_location = BooleanField(default=False)

    # Event-related fields
    posted_events = ListField(ReferenceField('BaseEvent'), default=[])
    liked_events = ListField(ReferenceField('BaseEvent'), default=[])
    reported_events = ListField(ReferenceField('BaseEvent'), default=[])

    # Comment related fields
    comments = ListField(ReferenceField('BaseComment'), default=[])

    # Friendship and relationship with other users
    friends = ListField(ReferenceField('Relationship'), default=[])
    friends_request_from = ListField(ReferenceField('Relationship'), default=[])
    friends_request_to = ListField(ReferenceField('Relationship'), default=[])
    blocking = ListField(ReferenceField('Relationship'), default=[])
    blocked_by = ListField(ReferenceField('Relationship'), default=[])
    ignoring = ListField(ReferenceField('User'), default=[])

    def get_simple(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "gender": self.gender,
            "display_name": self.display_name,
            "profile_url": self.profile_url,
            "location": self.location,
            "last_online": str(self.last_online)
        }

    def get_simple_header(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "display_name": self.display_name,
            "profile_url": self.profile_url,
        }

    def get_simple_relationship_drawer(self, username):
        relationship = Relationship.objects(between_users=[self.username, username]).first()
        if relationship is None:
            relationship = Relationship.objects(between_users=[username, self.username]).first()

        return {
            "id": str(self.id),
            "username": self.username,
            "gender": self.gender,
            "display_name": self.display_name,
            "profile_url": self.profile_url,
            "location": self.location,
            "last_online": str(self.last_online),
            "relationship": "Friend" if relationship in self.friends else "Normal"
        }

    def get_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "display_name": self.display_name,
            "nickname":self.nickname,
            "gender": self.gender,
            "profile_url": self.profile_url,
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
