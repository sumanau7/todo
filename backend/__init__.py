import os

from flask import Flask, request, current_app
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from config import Config


app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
ma = Marshmallow(app)
api = Api(app)


def create_app(config=Config):
    app.config.from_object(config)
    return app

app = create_app()


from todo import resources as todo_resources
from users import resources as users_resources


api.add_resource(users_resources.UserRegistration, "/user/registration")
api.add_resource(users_resources.UserLogin, "/user/login")
api.add_resource(users_resources.UserLogoutAccess, "/user/logout")
api.add_resource(users_resources.TokenRefresh, "/token/refresh")
api.add_resource(todo_resources.TodoResource, '/user/todo/', '/user/todo/<int:id>')
