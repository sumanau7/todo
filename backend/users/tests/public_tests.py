import mock
import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from backend import create_app, db

from backend.config import Config
import factoryboy
from backend.users import public


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests.db'


class PublicTests(unittest.TestCase): 

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_client = self.app.test_client()
        self.app_client.testing = True
        db.create_all()
        self.user = factoryboy.UserModelFactory()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_is_username_available(self):
        # Case 1: Username exists.
        available = public.is_username_available(self.user.username)
        self.assertFalse(available)
        # Case 2: Username doesn't exists.
        available = public.is_username_available('new_username')
        self.assertTrue(available)

    def test_get_user_by_username(self):
        # Case 1: Username exists.
        user = public.get_user_by_username(self.user.username)
        self.assertEqual(user, self.user)

        # Case 2: username doesn't exists.
        user = public.get_user_by_username('new_username')
        self.assertIsNone(user)

    @mock.patch('backend.users.public.create_access_and_refresh_token')
    def test_create_new_user(self, mock_create_access_token_and_refresh_token):
        username = 'new_username'
        password = 'new_password'
        mock_create_access_token_and_refresh_token.return_value = 'access', 'refresh'
        access_token, refresh_token = public.create_new_user(username, password)
        self.assertEqual(access_token, 'access')
        self.assertEqual(refresh_token, 'refresh')
        user = public.get_user_by_username(username)
        self.assertEqual(user.username, username)
        mock_create_access_token_and_refresh_token.assert_called_with(identity=username)

    @mock.patch('backend.users.public.create_refresh_token')
    @mock.patch('backend.users.public.create_access_token')
    def test_create_access_and_refresh_token(self, mock_create_access_token, mock_create_refresh_token):
        mock_create_access_token.return_value = 'access'
        mock_create_refresh_token.return_value = 'refresh'

        access_token, refresh_token = public.create_access_and_refresh_token('username')
        self.assertEqual(access_token, 'access')
        self.assertEqual(refresh_token, 'refresh')

        mock_create_refresh_token.assert_called_with('username')
        mock_create_access_token.assert_called_with('username')
