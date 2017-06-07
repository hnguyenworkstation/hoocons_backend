from flask import Flask
from flask_restful import Api
from services.authentication import *

import database.mlab as mlab
from services.user_services import *

app = Flask(__name__)
api = Api(app)
jwt = jwt_init(app)

mlab.connect()

########################################
# USER SERVICE APIs
########################################
api.add_resource(Register, "/api/register")
api.add_resource(CheckUsernameAvailability, "/api/user/availability")
api.add_resource(UpdateUserInfo, "/api/user/update/info")
api.add_resource(UpdatePassword, "/api/user/update/password")
api.add_resource(GetCurrentUserInfo, "/api/user/get/info")

if __name__ == '__main__':
    app.run()
