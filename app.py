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


'''########################################
 IDENTIFIED USER SERVICES APIs:
    @ finished features:
        + register/authenticate user
        + update user information
    @ future features:
########################################'''
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


'''########################################
 USERS SERVICES APIs:
    @ finished features:
        + Share/Clear Location
        + Get user around
        + Block/Unblock other user
        + Ignore/Un-ignore other user
    @ future features:
########################################'''
api.add_resource(ShareLocationRequest, "/api/user/post/location")
api.add_resource(ClearLocationRequest, "/api/user/remove/location")
api.add_resource(GetUserAroundRequest, "/api/user/get/around")

api.add_resource(BlockUserRequest, "/api/user/block")
api.add_resource(UnblockUserRequest, "/api/user/unblock")
api.add_resource(IgnoreUserRequest, "/api/user/ignore")


'''########################################
 FRIENDS SERVICES APIs:
    @ finished features:
        + Request friend
        + Accept/Deny friend request
        + Un-Friend
        + Get friend sublist
    @ future features:
        + get friend-request-received sublist
        + get friend-request-sent sublist
########################################'''
api.add_resource(SendFriendRequest, "/api/friend/request/send")
api.add_resource(AcceptFriendRequest, "/api/friend/request/accept")
api.add_resource(DeclineFriendRequest, "/api/friend/request/decline")
api.add_resource(UnfriendRequest, "/api/friend/request/remove")

api.add_resource(GetSubFriendList, "/api/friend/get/sublist")


'''########################################
 EVENTS SERVICES APIs:
    @ finished features:
        + Create/Delete event
        + Update event details
        + Like/Unlike event
        + Report event
        + get created-event sublist
    @ future features:
        + get friend's events sublist
########################################'''
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


'''########################################
 COMMENT SERVICES APIs:
    @ finished features:
        + add comment to an event
        + delete comment to an event
        + like/unlike comment
        + get comment sublist by time
    @ future features:
        + reply to a comment
########################################'''
api.add_resource(CreateCommentRequest, "/api/event/comment/create")
api.add_resource(DeleteCommentRequest, "/api/event/comment/delete")
api.add_resource(LikeCommentRequest, "/api/event/comment/like")
api.add_resource(UnlikeCommentRequest, "/api/event/comment/unlike")
api.add_resource(GetCommentRequest, "/api/comment/get/<_from>/<_to>")


'''########################################
 DANGER-ZONE SERVICES APIs:
 
 ***** THESE API BELOW HERE NEED TO BE RE-IMPLEMENTED
 BEFORE GOING TO BE USED IN CLIENTS
########################################'''
api.add_resource(DeleteUserAccount, "/api/user/delete")

if __name__ == '__main__':
    app.run()
