import json

from backend import create_app, db
import unittest

from backend.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests.db'


class TodoResourceTests(unittest.TestCase): 


    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_client = self.app.test_client()
        self.app_client.testing = True
        db.create_all()
        response = self.app_client.post(
            "/registration",
            data="{\"username\": \"test_4222\", \"password\": \"password\"}",
            content_type="application/json"
        )
        data = json.loads(response.data)
        print data
        self.access_token = data["access_token"]
        self.authorization = "Bearer {}".format(self.access_token)
        self.headers = {
            "Authorization": self.authorization,
            "Content-Type": "application/json"
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_todo_creation_and_get_integration(self):
        # Case 1: No saved TODO. GET TODO should return empty list.
        result = self.app_client.get('/todo/', headers=self.headers, follow_redirects=True)
        decoded_data =  json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(decoded_data, [])

        # Case 2: No saved TODO. Getting resource by invalid ID should raise BadRequest (400).
        result = self.app_client.get('/todo/100', headers=self.headers, follow_redirects=True)
        decoded_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(decoded_data, {"message": "Todo with ID 100 doesn't exists"})

        # # Case 3: Create Todo. Get all Todo.
        # todo_created = self.app_client.post(
        #     "/todo/1",
        #     data={"name": "test"},
        #     content_type="application/json",
        #     headers=self.headers
        # )
        # import pdb;pdb.set_trace()
        # decoded_data = json.loads(todo_created.data)
        # self.assertEqual(result.status_code, 200)
        # self.assertEqual(decoded_data, {})

        # # Case 4: Get all Todo.
        # result = self.app_client.get('/todo/', headers=self.headers, follow_redirects=True)
        # decoded_data =  json.loads(result.data)
        # self.assertEqual(result.status_code, 200)
        # self.assertEqual(decoded_data, [])
