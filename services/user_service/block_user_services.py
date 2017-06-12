from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

from static import status
from models.user import User
from models.relationship import *

from static import utils, app_constant


parser = reqparse.RequestParser()
parser.add_argument("username", type=str, location="json")


class BlockUserRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            body = parser.parse_args()
            username = body.username

            # Getting two users
            user = current_identity.user()
            blocking_user = User.objects(username=username).first()
            if user is None or blocking_user is None:
                return {"message": "failed to find user"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

            '''
                Getting the relationship between two users and go from there
                *** NOTES: need to sort the relationship twice because there might be the wrong other of between_users
            '''
            relationship = Relationship.objects(between_users=[user.username, username]).first()
            if relationship is None:
                relationship = Relationship.objects(between_users=[username, user.username]).first()

            # if there is no relationship, simply add both users to the relationship
            if relationship is None:
                blocked_request = Relationship(between_users=[user.username, username],
                                               status=app_constant.user_blocked).save()
                user.update(add_to_set__blocking=blocked_request)
                blocking_user.update(add_to_set__blocked_by=blocked_request)
                return {"message": "success"}, status.HTTP_200_OK

            '''
                If this the relationship exists, we have a friend request from them
                -- Blocking will also remove the user's request
            '''
            if relationship in user.friends_request_from:
                user.update(pull__friends_request_from=relationship)
                blocking_user.update(pull__friends_request_to=relationship)
                relationship.update(status=app_constant.user_blocked,
                                    time_of_action=datetime.utcnow())
                user.update(add_to_set__blocking=relationship)
                blocking_user.update(add_to_set__blocked_by=relationship)
                return {"message": "success"}, status.HTTP_200_OK

            if relationship in user.friends_request_to:
                user.update(pull__friends_request_to=relationship)
                blocking_user.update(pull__friends_request_from=relationship)
                relationship.update(status=app_constant.user_blocked,
                                    time_of_action=datetime.utcnow())
                user.update(add_to_set__blocking=relationship)
                blocking_user.update(add_to_set__blocked_by=relationship)
                return {"message": "success"}, status.HTTP_200_OK

            if relationship in user.friends:
                user.update(pull__friends=relationship)
                blocking_user.update(pull__friends=relationship)
                relationship.update(status=app_constant.user_blocked,
                                    time_of_action=datetime.utcnow())
                user.update(add_to_set__blocking=relationship)
                blocking_user.update(add_to_set__blocked_by=relationship)
                return {"message": "success"}, status.HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST


class UnblockUserRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            body = parser.parse_args()
            username = body.username

            # Getting two users
            user = current_identity.user()
            blocking_user = User.objects(username=username).first()
            if user is None or blocking_user is None:
                return {"message": "failed to find user"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

            '''
                Getting the relationship between two users and go from there
                *** NOTES: need to sort the relationship twice because there might be the wrong other of between_users
            '''
            relationship = Relationship.objects(between_users=[user.username, username]).first()
            if relationship is None:
                relationship = Relationship.objects(between_users=[username, user.username]).first()

            if relationship is None or relationship.status != app_constant.user_blocked:
                return {"message": "you are not blocking this user"}, status.HTTP_204_NO_CONTENT

            user.update(pull__blocking=relationship)
            blocking_user.update(pull__blocked_by=relationship)
            relationship.delete()
            return {"message": "success"}, status.HTTP_200_OK
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST
