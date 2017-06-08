from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

from static import status
from models.user import User
from models.relationship import *

from static import app_constant

parser = reqparse.RequestParser()
parser.add_argument("username", type=str, location="json")


class SendFriendRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            # Parsing JSON
            body = parser.parse_args()
            to_username = body.username

            user = current_identity.user()
            to_user = User.objects(username=to_username).first()

            if user is None or to_user is None:
                return {"message": "failed to find user"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

            ''' 
            **********
                If this user already sent you a request -- sent back to him a request means accept friendship
            **********
            '''
            if any(to_username in sublist for sublist in user.friends_request_from) is True:
                # Getting the relationship object
                relationship = Relationship.objects(between_users=[user.username, to_username]).first()
                if relationship is None:
                    relationship = Relationship.objects(between_users=[to_username, user.username]).first()
                    if relationship is None:
                        return {"message": "unable to find friend request"}, status.HTTP_204_NO_CONTENT

                # If the friend request found
                user.update(pull__friends_request_from=relationship)
                to_user.update(pull__friends_request_to=relationship)

                relationship.update(time_of_action=datetime.utcnow(), status=app_constant.IS_FRIEND)
                user.update(add_to_set__friends=relationship)
                to_user.update(add_to_set__friends=relationship)

            ''' 
            **********
                If you already sent this user a friend request before
            **********
            '''
            if any(to_username in sublist for sublist in user.friends_request_to) is True:
                return {"message": "request already sent"}, status.HTTP_201_CREATED

            '''
            **********
                Nothing happened before, send branch new request to the user
            **********
            '''
            friend_request = Relationship(between_users=[user.username, to_username],
                                          status=app_constant.FRIEND_REQUESTING).save()
            user.update(add_to_set__friends_request_to=friend_request)
            to_user.update(add_to_set__friends_request_from=friend_request)
            return {"message": "success"}, status.HTTP_200_OK
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


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
                return {"message": "failed to find user"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

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

                relationship.update(time_of_action=datetime.utcnow(), status=app_constant.IS_FRIEND)
                user.update(add_to_set__friends=relationship)
                from_user.update(add_to_set__friends=relationship)
                return {"message": "success"}, status.HTTP_200_OK
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
                return {"message": "failed to find user"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

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
                relationship.delete()
                return {"message": "success"}, status.HTTP_200_OK
            else:
                return {"message": "unable to find user request"}, status.HTTP_204_NO_CONTENT
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


class UnfriendRequest(Resource):
    @jwt_required()
    def delete(self):
        try:
            # Parsing JSON
            body = parser.parse_args()
            friend_username = body.username

            user = current_identity.user()
            friend = User.objects(username=friend_username).first()

            if user is None or friend is None:
                return {"message": "failed to find user"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

            '''
                Checking if the requesting user is in the friend list
            '''
            if any(friend_username in sublist for sublist in user.friends) is True:
                # Getting the relationship object
                relationship = Relationship.objects(between_users=[user.username, friend_username]).first()
                if relationship is None:
                    relationship = Relationship.objects(between_users=[friend_username, user.username]).first()
                    if relationship is None:
                        return {"message": "unable to find relationship"}, status.HTTP_204_NO_CONTENT

                # If the friend request found
                user.update(pull__friends=relationship)
                friend.update(pull__friends=relationship)
                relationship.delete()
                return {"message": "success"}, status.HTTP_200_OK
            else:
                return {"message": "not active friend"}
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST

