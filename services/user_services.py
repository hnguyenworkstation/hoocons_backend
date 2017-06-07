from datetime import datetime

from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

import static.utils
from models.user import User


class CheckUsernameAvailability(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("username", type=str, location="json")
            body = parser.parse_args()
            user = User.objects(username=body.username).first()
            if user is None:
                return {"message": "available"}, 200
            return {"message": "existed"}, 202
        except Exception as e:
            return {"message": str(e)}, 401


class UpdateUserInfo(Resource):
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        user = current_identity.user()
        if user is None:
            return {"message": "null"}, 401
        parser.add_argument("profile_url", type=str, location="json")
        parser.add_argument("gender", type=str, location="json")
        parser.add_argument("display_name", type=str, location="json")
        parser.add_argument("birthday", type=str, location="json")
        parser.add_argument("longitude", type=float, location="json")
        parser.add_argument("latitude", type=float, location="json")
        body = parser.parse_args()
        try:
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

            # Getting user birthday
            birthday = body.birthday
            if birthday is not None and len(birthday) > 0:
                user.birthday = birthday

            # Getting the location
            latitude = body.latitude
            longitude = body.longitude
            if latitude is not None and latitude > -181 and (longitude is not None and longitude > -181):
                user.location = [longitude, latitude]
        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 401
