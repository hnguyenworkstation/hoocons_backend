from datetime import datetime

from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

import static.utils as utils
import static.status as status
from models.user import User
from models.comment import BaseComment
from models.base_event import BaseEvent
from models.action import BaseAction
from models.relationship import Relationship


GENDER = ('Male', 'Female', 'Other')


class CheckUsernameAvailability(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("username", type=str, location="json")
            body = parser.parse_args()
            user = User.objects(username=body.username).first()
            if user is None:
                return {"message": "available"}, status.HTTP_200_OK
            return {"message": "existed"}, status.HTTP_201_CREATED
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


class CheckNicknameAvailability(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("nickname", type=str, location="json")
            body = parser.parse_args()
            user = User.objects(nickname=body.nickname).first()
            if user is None:
                return {"message": "available"}, status.HTTP_200_OK
            return {"message": "existed"}, status.HTTP_201_CREATED
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


class UpdateUserInfo(Resource):
    @jwt_required()
    def put(self):
        # Getting current identified user
        parser = reqparse.RequestParser()
        user = current_identity.user()
        if user is None:
            return {"message": "null"}, status.HTTP_401_UNAUTHORIZED

        try:
            # Update user info
            parser.add_argument("profile_url", type=str, location="json")
            parser.add_argument("gender", type=str, location="json")
            parser.add_argument("display_name", type=str, location="json")
            parser.add_argument("nickname", type=str, location="json")
            parser.add_argument("birthday", type=str, location="json")
            parser.add_argument("longitude", type=float, location="json")
            parser.add_argument("latitude", type=float, location="json")
            body = parser.parse_args()

            # Getting the gender
            gender = body.gender
            if gender is not None and len(gender) > 0:
                user.gender = gender

            # Getting profile Url
            profile_url = body.profile_url
            if profile_url is not None and len(profile_url) > 0:
                user.profile_url = profile_url

            # Getting display name
            display_name = body.display_name
            if display_name is not None and len(display_name) > 0:
                user.display_name = display_name

            # Getting nickname
            nickname = body.nickname
            if nickname is not None and len(nickname) > 0:
                user.nickname = nickname

            # Getting user birthday
            birthday = body.birthday
            if birthday is not None and len(birthday) > 0:
                user.birthday = utils.date_from_iso8601(birthday)

            # Getting the location
            latitude = body.latitude
            longitude = body.longitude
            if latitude is not None and latitude > -181 and (longitude is not None and longitude > -181):
                user.location = [longitude, latitude]

            user.save()
            user.update(last_online=datetime.utcnow())
            return user.get_json(), status.HTTP_200_OK
        except Exception as e:
            print(str(e))
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


class UpdateDisplayName(Resource):
    @jwt_required()
    def put(self):
        # Getting current identified user
        user = current_identity.user()
        if user is None:
            return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

        # Try to save user display name
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("display_name", type=str, location="json")
            body = parser.parse_args()
            display_name = body.display_name
            if display_name is not None and len(display_name) > 0:
                user.display_name = display_name
                user.save()
                user.update(last_online=datetime.utcnow())
                return status.HTTP_200_OK
            else:
                return {"message": "Invalid display name"}, status.HTTP_417_EXPECTATION_FAILED
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


class UpdateProfileUrl(Resource):
    @jwt_required()
    def put(self):
        # Getting current identified user
        user = current_identity.user()
        if user is None:
            return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

        # Try to save user display name
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("profile_url", type=str, location="json")
            body = parser.parse_args()
            profile_url = body.profile_url
            if profile_url is not None and len(profile_url) > 0:
                user.profile_url = profile_url
                user.save()
                user.update(last_online=datetime.utcnow())
                return status.HTTP_200_OK
            else:
                return {"message": "Invalid Profile Url"}, status.HTTP_417_EXPECTATION_FAILED
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


class UpdateGender(Resource):
    @jwt_required()
    def put(self):
        # Getting current identified user
        user = current_identity.user()
        if user is None:
            return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

        # Try to save user display name
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("gender", type=str, location="json")
            body = parser.parse_args()
            gender = body.gender
            if gender is not None and len(gender) > 0 and gender in GENDER:
                user.gender = gender
                user.save()
                user.update(last_online=datetime.utcnow())
                return status.HTTP_200_OK
            else:
                return {"message": "Invalid gender! Gender must be one of 'Male', 'Female', 'Other'"},\
                       status.HTTP_417_EXPECTATION_FAILED
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


class UpdateNickname(Resource):
    @jwt_required()
    def put(self):
        # Getting current identified user
        user = current_identity.user()
        if user is None:
            return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

        # Try to save user display name
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("nickname", type=str, location="json")
            body = parser.parse_args()
            nickname = body.nickname
            if nickname is not None and len(nickname) > 0:
                user.nickname = nickname
                user.save()
                user.update(last_online=datetime.utcnow())
                return status.HTTP_200_OK
            else:
                return {"message": "Invalid nickname"}, status.HTTP_417_EXPECTATION_FAILED
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


class UpdateBirthday(Resource):
    @jwt_required()
    def put(self):
        # Getting current identified user
        user = current_identity.user()
        if user is None:
            return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

        # Try to save user display name
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("birthday", type=str, location="json")
            body = parser.parse_args()
            birthday = body.birthday
            if birthday is not None and len(birthday) > 0:
                user.birthday = utils.date_from_iso8601(birthday)
                user.save()
                user.update(last_online=datetime.utcnow())
                return status.HTTP_200_OK
            else:
                return {"message": "Invalid Birthday"}, status.HTTP_417_EXPECTATION_FAILED
        except Exception as e:
            return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


class UpdatePassword(Resource):
    @jwt_required()
    def put(self):
        # Getting current identified user
        parser = reqparse.RequestParser()
        user = current_identity.user()

        try:
            # Getting new password and update
            parser.add_argument("password", type=str, location="json")
            body = parser.parse_args()
            password = body.password
            if password is not None and len(password) > 0:
                user.update(last_online=datetime.utcnow(), password=password)
                return {"message": "success"}, status.HTTP_200_OK
            return {"message": "invalid password"}, 204
        except Exception as e:
            return {"message": str(e)}, 401


class ResetPasswordRequest(Resource):
    # This method is used when user forgets password and want to reset it
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("username", type=str, location="json")
            parser.add_argument("password", type=str, location="json")  # this is new password send to server
            body = parser.parse_args()
            password = body.password
            username = body.username

            user = User.objects(username=username).first()
            if user is None:
                return {"message": "not registered yet"}, status.HTTP_204_NO_CONTENT

            if password is not None and len(password) > 0:
                user.update(password=password)
                return {"message": "success"}, status.HTTP_200_OK
            return {"message": "invalid password"}, 204
        except Exception as e:
            return {"message": str(e)}, 401


class GetCurrentUserInfo(Resource):
    @jwt_required()
    def get(self):
        try:
            user = current_identity.user()
            if user is not None:
                user.update(last_online=datetime.utcnow())
                return user.get_json(), status.HTTP_200_OK
            return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED
        except Exception as e:
            return {"message": str(e)}


class DeleteUserAccount(Resource):
    @jwt_required()
    def delete(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            # Delete everything created by the current user
            # Todo: Need to delete references of things created by this user
            for action in BaseAction.objects(by_user=user):
                action.delete()

            for comment in BaseComment.objects(create_by=user):
                comment.delete()

            for event in BaseEvent.objects(create_by=user):
                event.delete()

            user.delete()
            return {"message": "delete account complete"}, status.HTTP_200_OK
        except Exception as e:
            return {"message": str(e)}
