import json

from backend import create_app, db
import unittest

from backend.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests.db'


class UserRegistrationTests(unittest.TestCase): 


    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_client = self.app.test_client()
        self.app_client.testing = True
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        response = self.app_client.post(
            "/registration",
            data="{\"username\": \"test\", \"password\": \"password\"}",
            content_type="application/json"
        )
        data = json.loads(response.data)
        keys = ["access_token", "refresh_token", "username"]
        self.assertEqual(set(keys), set(data.keys()))


class UserLoginTests(unittest.TestCase): 

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_client = self.app.test_client()
        self.app_client.testing = True
        db.create_all()
        response = self.app_client.post(
            "/registration",
            data="{\"username\": \"test\", \"password\": \"password\"}",
            content_type="application/json"
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_user(self):
        response = self.app_client.post(
            "/login",
            data="{\"username\": \"test\", \"password\": \"password\"}",
            content_type="application/json"
        )
        data = json.loads(response.data)
        keys = ["access_token", "refresh_token", "username"]
        self.assertEqual(set(keys), set(data.keys()))


class UserLogoutTests(unittest.TestCase): 

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_client = self.app.test_client()
        self.app_client.testing = True
        db.create_all()
        response = self.app_client.post(
            "/registration",
            data="{\"username\": \"test\", \"password\": \"password\"}",
            content_type="application/json"
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def test_logout_user(self):
    #     response = self.app_client.post(
    #         "/logout",
    #         data="{\"username\": \"test\", \"password\": \"password\"}",
    #         content_type="application/json"
    #     )
    #     data = json.loads(response.data)
    #     keys = ["access_token", "refresh_token", "username"]
    #     self.assertEqual(set(keys), set(data.keys()))
