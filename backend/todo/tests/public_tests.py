import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from backend import create_app, db

from backend.config import Config
import factoryboy
from backend.todo import public

from backend.users.tests import factoryboy as user_factoryboy

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests.db'


class PublicTests(unittest.TestCase): 

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_client = self.app.test_client()
        self.app_client.testing = True
        db.create_all()
        self.user = user_factoryboy.UserModelFactory()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_todo_by_id(self):
        todo = factoryboy.TodoFactory(user_id=self.user.id, name='test')
        db.session.commit()
        todo_from_db = public.get_todo_by_id(todo.id)
        self.assertEqual(todo, todo_from_db)

    def test_get_all_todos_for_user(self):
        # Case 1: No Todos in database.
        todos = public.get_all_todos_for_user(self.user.id)
        self.assertEqual(todos, [])

        # Case 2: Todos exists for user in database.
        todo_1 = factoryboy.TodoFactory(user_id=self.user.id, name='test_1')
        todo_2 = factoryboy.TodoFactory(user_id=self.user.id, name='test_2')
        todos = public.get_all_todos_for_user(self.user.id)
        self.assertEqual(todos, [todo_1, todo_2])

    def test_create_todo_for_user(self):
        public.create_todo_for_user('test', self.user.id)
        todos = public.get_all_todos_for_user(self.user.id)
        self.assertEqual(todos[0].name, 'test')

    def test_delete_todo_for_user(self):
        self.unauthorized_user = user_factoryboy.UserModelFactory()
        todo = factoryboy.TodoFactory(user_id=self.user.id, name='test_1')
        db.session.commit()
        # Case 1: Another user trying to delete todo of another user.
        response = public.delete_todo_for_user(todo.id, self.unauthorized_user.id)
        self.assertIsNone(response)

        # Case 2: ID doesn't exists.
        fake_id = 100000
        response = public.delete_todo_for_user(fake_id, self.user.id)
        self.assertIsNone(response)

        # Case 3: Delete todo.
        response = public.delete_todo_for_user(todo.id, self.user.id)
        deleted = 1
        self.assertEqual(response, deleted)
