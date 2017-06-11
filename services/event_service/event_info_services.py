from datetime import datetime

from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

import static.status as status
from models.base_event import BaseEvent


class CreateEventRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            parser = reqparse.RequestParser()
            parser.add_argument("text_context", type=str, location="json")
            parser.add_argument("images", type=list, location="json")
            parser.add_argument("contain_event", type=str, location="json")
            parser.add_argument("privacy", type=str, location="json")
            parser.add_argument("longitude", type=float, location="json")
            parser.add_argument("latitude", type=float, location="json")
            parser.add_argument("tags", type=list, location="json")
            body = parser.parse_args()

            event = BaseEvent(create_by=user, text_context=body.text_context,
                              images=body.images, contain_event=body.contain_event,
                              privacy=body.privacy, location=[body.longitude, body.latitude],
                              tags=body.tags).save()
            user.update(add_to_set__posted_events=event, last_online=datetime.utcnow())
            return event.get_initial_json(), status.HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST


class UpdateEventRequest(Resource):
    @jwt_required()
    def put(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            parser = reqparse.RequestParser()
            parser.add_argument("event_id", type=str, location="json")
            parser.add_argument("text_context", type=str, location="json")
            parser.add_argument("images", type=list, location="json")
            parser.add_argument("contain_event", type=str, location="json")
            parser.add_argument("privacy", type=str, location="json")
            parser.add_argument("longitude", type=float, location="json")
            parser.add_argument("latitude", type=float, location="json")
            parser.add_argument("tags", type=list, location="json")
            body = parser.parse_args()

            event = BaseEvent.objects(id=body.event_id).first()
            if event is None or event not in user.posted_events:
                return {"message": "no permission to delete"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

            event.update(text_context=body.text_context, images=body.images, contain_event=body.contain_event,
                         privacy=body.privacy, location=[body.longitude, body.latitude], tags=body.tags)
            user.update(last_online=datetime.utcnow())
            return event.get_complete_json(), status.HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST


class UpdateTextEventRequest(Resource):
    @jwt_required()
    def put(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            parser = reqparse.RequestParser()
            parser.add_argument("event_id", type=str, location="json")
            parser.add_argument("text_context", type=str, location="json")
            body = parser.parse_args()

            event = BaseEvent.objects(id=body.event_id).first()
            if event is None or event not in user.posted_events:
                return {"message": "no permission to delete"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

            event.update(text_context=body.text_context)
            user.update(last_online=datetime.utcnow())
            return event.get_complete_json(), status.HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST


class DeleteEventRequest(Resource):
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
                return {"message": "event does not exists"}, status.HTTP_501_NOT_IMPLEMENTED

            if event not in user.posted_events:
                return {"message": "no permission to delete"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

            # Enough permission and information -> remove event
            user.update(pull__posted_events=event, last_online=datetime.utcnow())
            event.delete()
            return {"message": "success"}, status.HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

