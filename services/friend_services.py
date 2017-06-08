from datetime import datetime

from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

from static import status
from models.user import User
from models.relationship import *

from static import utils, app_constant

parser = reqparse.RequestParser()
parser.add_argument("username", type=str, location="json")


class AcceptFriendRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            # Parsing JSON
            body = parser.parse_args()
            from_username = body.username

            user = current_identity.user()
            from_user = User.objects(username=from_username).first()

            if user is None or from_user is None:
                return {"message": "failed to find user"}, status.HTTP_401_UNAUTHORIZED

            # Checking if this user requested friend yet
            if any(from_username in sublist for sublist in user.friends_request_from) is True:
                # Getting the relationship object
                relationship = Relationship.objects(between_users=[user.username, from_username]).first()
                if relationship is None:
                    relationship = Relationship.objects(between_users=[from_username, user.username]).first()
                    if relationship is None:
                        return {"message": "unable to find friend request"}, status.HTTP_204_NO_CONTENT

                # If the friend request found
                user.update(pull__friends_request_from=relationship)
                from_user.update(pull__friends_request_to=relationship)

                relationship.update(date_of_action=datetime.utcnow(), status=app_constant.IS_FRIEND)
                user.update(add_to_set__friends=relationship)
                from_user.update(add_to_set__friends=relationship)
            else:
                return {"message": "unable to find user request"}, status.HTTP_204_NO_CONTENT
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


class DeclineFriendRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            # Parsing JSON
            body = parser.parse_args()
            from_username = body.username

            user = current_identity.user()
            from_user = User.objects(username=from_username).first()

            if user is None or from_user is None:
                return {"message": "failed to find user"}, status.HTTP_401_UNAUTHORIZED

            # Checking if this user requested friend yet
            if any(from_username in sublist for sublist in user.friends_request_from) is True:
                # Getting the relationship object
                relationship = Relationship.objects(between_users=[user.username, from_username]).first()
                if relationship is None:
                    relationship = Relationship.objects(between_users=[from_username, user.username]).first()
                    if relationship is None:
                        return {"message": "unable to find friend request"}, status.HTTP_204_NO_CONTENT

                # If the friend request found
                user.update(pull__friends_request_from=relationship)
                from_user.update(pull__friends_request_to=relationship)
            else:
                return {"message": "unable to find user request"}, status.HTTP_204_NO_CONTENT
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST

