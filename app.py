from flask import Flask
from flask_restful import Api

from services.common_service.authentication import *

from services.event_service.event_info_services import *
from services.event_service.event_request_services import *
from services.event_service.comment_services import *

from services.friend_service.friend_request_services import *
from services.friend_service.friend_services import *

from services.user_service.block_user_services import *
from services.user_service.ignore_user_services import *
from services.user_service.user_info_services import *
from services.user_service.user_request_services import *

app = Flask(__name__)
api = Api(app)
jwt = jwt_init(app)

mlab.connect()


########################################
# USER INFO SERVICE APIs
########################################
api.add_resource(Register, "/api/register")
api.add_resource(CheckUsernameAvailability, "/api/user/availability")
api.add_resource(UpdateUserInfo, "/api/user/update/info")
api.add_resource(UpdatePassword, "/api/user/update/password")
api.add_resource(UpdateDisplayName, "/api/user/update/display_name")
api.add_resource(UpdateNickname, "/api/user/update/nickname")
api.add_resource(UpdateProfileUrl, "/api/user/update/profile_url")
api.add_resource(UpdateBirthday, "/api/user/update/birthday")
api.add_resource(UpdateGender, "/api/user/update/gender")
api.add_resource(GetCurrentUserInfo, "/api/user/get/info")


########################################
# USER SERVICES APIs
########################################
api.add_resource(ShareLocationRequest, "/api/user/post/location")
api.add_resource(ClearLocationRequest, "/api/user/remove/location")
api.add_resource(GetUserAroundRequest, "/api/user/get/around")


########################################
# USER BLOCKING SERVICES APIs
########################################
api.add_resource(BlockUserRequest, "/api/user/block")
api.add_resource(UnblockUserRequest, "/api/user/unblock")
api.add_resource(IgnoreUserRequest, "/api/user/ignore")


########################################
# FRIEND SERVICE APIs
########################################
api.add_resource(SendFriendRequest, "/api/friend/request/send")
api.add_resource(AcceptFriendRequest, "/api/friend/request/accept")
api.add_resource(DeclineFriendRequest, "/api/friend/request/decline")
api.add_resource(UnfriendRequest, "/api/friend/request/remove")

api.add_resource(GetSubFriendList, "/api/friend/get/sublist")


########################################
# EVENT SERVICES APIs
########################################
api.add_resource(CreateEventRequest, "/api/event/create")
api.add_resource(UpdateEventRequest, "/api/event/update")
api.add_resource(UpdateTextEventRequest, "/api/event/update/text")
api.add_resource(UpdateLocationEventRequest, "/api/event/update/location")
api.add_resource(UpdateTagsEvent, "/api/event/update/tags")
api.add_resource(DeleteEventRequest, "/api/event/delete")
api.add_resource(ReportEvent, "/api/event/report")

api.add_resource(GetCreatedEvent, "/api/event/get/<_from>/<_to>")
api.add_resource(LikeEventRequest, "/api/event/like")
api.add_resource(UnlikeEventRequest, "/api/event/unlike")

########################################
# COMMENT SERVICES APIs
########################################
api.add_resource(CreateCommentRequest, "/api/event/create/comment")

if __name__ == '__main__':
    app.run()
