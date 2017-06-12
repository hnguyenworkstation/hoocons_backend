from datetime import *
from mongoengine import *
from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource
from static import app_constant, status

from models.comment import BaseComment
from models.base_event import BaseEvent
from models.action import BaseAction


class CreateCommentRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            parser = reqparse.RequestParser()
            parser.add_argument("event_id", type=str, location="json")
            parser.add_argument("text_content", type=str, location="json")
            parser.add_argument("image", type=str, location="json")
            body = parser.parse_args()

            event_id = body.event_id
            text_content = body.text_content
            image = body.image

            # Now file the event and then add comment to it
            event = BaseEvent.objects(id=event_id).first()
            if event is None:
                return {"message": "event not found"}, status.HTTP_204_NO_CONTENT

            comment = BaseComment(create_by=user, text_content=text_content, image=image).save()
            event.update(add_to_set__comments=comment)

            # Now create an action
            action = BaseAction(by_user=user, action_type=app_constant.action_comment_event, target=event.id,
                                content=comment.id, action_priority=app_constant.priority_low).save()
            user.update(last_online=datetime.utcnow(), add_to_set__recent_actions=action)

            return {"message": "request success"}, status.HTTP_200_OK
        except ValueError as err:
            return {"error": str(err)}, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST


class DeleteCommentRequest(Resource):
    @jwt_required()
    def delete(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            parser = reqparse.RequestParser()
            parser.add_argument("event_id", type=str, location="json")
            parser.add_argument("comment_id", type=str, location="json")
            body = parser.parse_args()

            event_id = body.event_id
            comment_id = body.comment_id

            # Now file the event and then add comment to it
            event = BaseEvent.objects(id=event_id).first()
            if event is None:
                return {"message": "event not found"}, status.HTTP_204_NO_CONTENT

            comment = BaseComment.objects(id=comment_id).first()
            if comment is None:
                return {"message": "unable to fine event"}, status.HTTP_204_NO_CONTENT

            event.update(pull__comments=comment)
            user.update(last_online=datetime.utcnow())
            comment.delete()
            return {"message": "request success"}, status.HTTP_200_OK
        except ValueError as err:
            return {"error": str(err)}, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST
