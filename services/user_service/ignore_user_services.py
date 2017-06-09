from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

from static import status
from models.user import *


parser = reqparse.RequestParser()
parser.add_argument("username", type=str, location="json")


class IgnoreUserRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            body = parser.parse_args()
            username = body.username

            # Getting current user
            user = current_identity.user()
            ignore_ppl = User.objects(username=username).first()
            if user is None or ignore_ppl is None:
                return {"message": "failed to find user"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

            if ignore_ppl in user.ignoring:
                return {"message": "already ignored"}, status.HTTP_201_CREATED

            user.update(add_to_set__ignoring=ignore_ppl)
            return {"message": "success"}, status.HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    @jwt_required()
    def delete(self):
        try:
            body = parser.parse_args()
            username = body.username

            # Getting current user
            user = current_identity.user()
            ignore_ppl = User.objects(username=username).first()
            if user is None or ignore_ppl is None:
                return {"message": "failed to find user"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

            if ignore_ppl not in user.ignoring:
                return {"message": "not ignore this person"}, status.HTTP_204_NO_CONTENT

            user.update(pull__ignoring=ignore_ppl)
            return {"message": "success"}, status.HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST
