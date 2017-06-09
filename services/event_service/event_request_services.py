from datetime import datetime

from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

import static.status as status
from models.base_event import BaseEvent


class GetCreatedEvent(Resource):
    @jwt_required()
    def get(self, _from, _to):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED
            '''
            parser = reqparse.RequestParser()
            parser.add_argument("from_pos", type=int, location="headers")
            parser.add_argument("to_pos", type=int, location="headers")
            body = parser.parse_args()
    
            _from = body.from_pos
            _to = body.to_pos
            '''
            try:
                _from = int(_from)
                _to = int(_to)
            except ValueError as err:
                pass

            if _from > len(user.posted_events):
                return [], status.HTTP_200_OK
            elif _to >= len(user.posted_events):
                return [event.get_complete_json() for event in user.posted_events[_from:]], status.HTTP_200_OK
            else:
                return [event.get_complete_json() for event in user.posted_events[_from:_to]], status.HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST
