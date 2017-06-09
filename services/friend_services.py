from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

from static import status


class GetSubFriendList(Resource):
    @jwt_required()
    def post(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "failed to find user"}, status.HTTP_401_UNAUTHORIZED

            parser = reqparse.RequestParser()
            parser.add_argument("from_pos", type=int, location="json")
            parser.add_argument("to_pos", type=int, location="json")
            body = parser.parse_args()

            # Getting the values
            _from_pos = body.from_pos
            _to_pos = body.to_pos

            return [friend.get_simple() for friend in user.friends[_from_pos:_to_pos]]
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST
