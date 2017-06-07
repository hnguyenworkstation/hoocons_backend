from flask import Flask
from flask_restful import Api

from services.authentication import *

import database.mlab as mlab

app = Flask(__name__)
api = Api(app)
jwt = jwt_init(app)

mlab.connect()

api.add_resource(Register, "/register")

if __name__ == '__main__':
    app.run()
