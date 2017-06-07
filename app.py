from flask import Flask
from flask_restful import Api

from services.authentication import *
from services.user_services import *

import database.mlab as mlab

app = Flask(__name__)
api = Api(app)
jwt = jwt_init(app)

mlab.connect()

########################################
# USER SERVICE APIS
########################################
api.add_resource(Register, "/api/register")
api.add_resource(CheckUsernameAvailability, "/api/user/availability")
if __name__ == '__main__':
    app.run()
