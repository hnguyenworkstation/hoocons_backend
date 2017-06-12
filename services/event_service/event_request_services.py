from datetime import datetime

from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

import static.status as status
from static import app_constant
from models.base_event import BaseEvent
from models.action import BaseAction


class GetCreatedEvent(Resource):
    @jwt_required()
    def get(self, _from, _to):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            try:
                _from = int(_from)
                _to = int(_to)
            except ValueError as err:
                pass

            user.update(last_online=datetime.utcnow())
            if _from > len(user.posted_events):
                return [], status.HTTP_200_OK
            elif _to >= len(user.posted_events):
                return [event.get_complete_json() for event in user.posted_events[_from:]], status.HTTP_200_OK
            else:
                return [event.get_complete_json() for event in user.posted_events[_from:_to]], status.HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST


class LikeEventRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            parser = reqparse.RequestParser()
            parser.add_argument("event_id", type=str, location="json")

            body = parser.parse_args()
            event = BaseEvent.objects(id=body.event_id).first()
            if event is None:
                return {"message": "failed to find event"}, status.HTTP_204_NO_CONTENT

            event.update(add_to_set__liked_by=user)

            # Now create an action
            action = BaseAction(by_user=user, action_type=app_constant.action_like_event, target=event.id,
                                action_priority=app_constant.priority_low).save()
            user.update(add_to_set__recent_actions=action, last_online=datetime.utcnow())
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST


class UnlikeEventRequest(Resource):
    @jwt_required()
    def delete(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            parser = reqparse.RequestParser()
            parser.add_argument("event_id", type=str, location="json")

            body = parser.parse_args()
            event = BaseEvent.objects(id=body.event_id).first()
            if event is None:
                return {"message": "failed to find event"}, status.HTTP_204_NO_CONTENT

            if user not in event.liked_by:
                return {"message": "you did not like the event"}, status.HTTP_204_NO_CONTENT

            event.update(pull__liked_by=user)
            user.update(last_online=datetime.utcnow())
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST