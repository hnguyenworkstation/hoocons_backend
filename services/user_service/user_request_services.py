from datetime import datetime

from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource
from models.user import User

import static.status as status
from models.base_event import BaseEvent
from models.relationship import Relationship


class GetUserAroundRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            parser = reqparse.RequestParser()
            parser.add_argument("longitude", type=float, location="json")
            parser.add_argument("latitude", type=float, location="json")
            parser.add_argument("from_pos", type=int, location="json")
            parser.add_argument("to_pos", type=int, location="json")
            body = parser.parse_args()

            try:
                _from = int(body.from_pos)
                _to = int(body.to_pos)

                user_around = User.objects(location__near=[body.longitude, body.latitude], location__max_distance=1000)

                '''
                    Now try to remove all blocked/blocking/ignoring person
                    -- Decided to show ignoring user on the list around: 6/11/2017
                '''
                for a_user in user_around:
                    relationship = Relationship.objects(between_users=[user.username, a_user.username]).first()
                    if relationship is None:
                        relationship = Relationship.objects(between_users=[a_user.username, user.username]).first()

                    if relationship in user.blocked_by or relationship in user.blocking:
                        user_around.remove(a_user)

                if _from > len(user_around):
                    return [], status.HTTP_200_OK
                elif _to >= len(user_around):
                    return [user.get_simple_relationship_drawer(a_user.username)
                            for a_user in user_around[_from:]], status.HTTP_200_OK
                else:
                    return [user.get_simple_relationship_drawer(a_user.username)
                            for a_user in user_around[_from:_to]], status.HTTP_200_OK
            except ValueError as err:
                return {"error": str(err)}, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST


