import datetime

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.channel import *

from static import status


class CreateChannelRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            user = current_identity.user()
            if user is None:
                return {"message": "Unable to find user information"}, status.HTTP_401_UNAUTHORIZED

            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, location="json")
            parser.add_argument("subname", type=str, location="json")
            parser.add_argument("profile_url", type=str, location="json")
            parser.add_argument("wallpaper_url", type=str, location="json")
            parser.add_argument("description", type=str, location="json")
            parser.add_argument("tags", type=list, location="json")
            body = parser.parse_args()

            name = body.name
            subname = body.subname
            description = body.description
            profile_url = body.profile_url
            wallpaper_url = body.wallpaper_url
            tags = body.tags

            channel = BaseChannel(created_by=user, owner=user, name=name, subname=subname, description=description,
                                  profile_url=profile_url, wallpaper_url=wallpaper_url, tags=tags).save()

            user.update(last_online=datetime.utcnow(), add_to_set__owner_channels=channel,
                        add_to_set__created_channels=channel)
            return {"message": "request success"}, status.HTTP_200_OK
        except ValueError as err:
            return {"error": str(err)}, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST
