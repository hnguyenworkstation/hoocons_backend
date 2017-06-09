from datetime import datetime

from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource

import static.status as status
from models.base_event import BaseEvent


class GetCreatedEvent(Resource):
    @jwt_required
    def get(self):
        user = current_identity.user()
        if user is None:
            return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

        parser = reqparse.RequestParser()
        parser.add_argument("from_pos", type=int, location="json")
        parser.add_argument("to_pos", type=int, location="json")
        body = parser.parse_args()

        _from = body.from_pos
        _to = body.to_pos

        if _from > len(self.posted_events):
            return [], status.HTTP_200_OK
        elif _to >= len(self.posted_events):
            return [event for event in self.posted_events[_from:]], status.HTTP_200_OK
        else:
            return [event for event in self.posted_events[_from:_to]], status.HTTP_200_OK

