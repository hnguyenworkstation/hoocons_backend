from datetime import datetime

from mongoengine import *
from static import app_constant


class BaseAction(Document):
    """
        @by_user: Who makes this action
        @action_type = LIKE, SHARE, MAKING FRIENDS, POST EVENT ....
        @target: Id of target (event, user)
        @with_content: Maybe NONE since content only available for comment
        @action_priority: this field determine how we order the list of events shows on homepage
    """
    by_user = ReferenceField('User', required=True)
    action_type = StringField(default="", choices=app_constant.ACTION_TYPES)
    date_of_action = DateTimeField(default=datetime.utcnow())
    target = StringField(default="")
    with_content = StringField(default="")
    action_priority = StringField(default="", choices=app_constant.ACTION_PRIORITY)
    is_scrolled_by = BooleanField(default=False)
    is_viewed = BooleanField(default=False)

    def get_complete_json(self):
        target = Document.objects(id=self.target).first()
        with_content = Document.objects(id=self.with_content).first()

        return {
            "id": self.id,
            "by_user": self.by_user.get_simple_header(),
            "target": "" if target is None else target.get_complete_json(),
            "with_content": "" if with_content is None else with_content.get_complete_json(),
            "action_priority": self.action_priority,
            "is_scrolled_by": self.is_scrolled_by,
            "is_viewed": self.is_viewed
        }
