import json
import os
from datetime import timedelta, datetime
from unittest.mock import patch, MagicMock

import jwt
from flask_testing import TestCase

from api.user.errors import UserEmailExistsException, UserNameExistsException, EmailNotValidException, \
    UnauthorizedException, UserNameInvalidException, PasswordInvalidException
from app import app_main
from constants.urls import API_USER_REGISTER, API_USER_LOGIN
from model.user_model import *
from resources.resources_paths import TEST_QUERY_DB_PATH, TEST_USER_DB_PATH
from services.config import config_service
from services.user import user_service
from test_utils import create_test_app, ProtectedTestRoute


@patch('app.app_main.logger', MagicMock())
@patch('services.config.config_service.get_user_db_path', MagicMock(return_value=TEST_USER_DB_PATH))
@patch('services.config.config_service.get_app_key', MagicMock(return_value='mock_key'))
class TestUserService(TestCase):
    def create_app(self):
        return create_test_app(TEST_USER_DB_PATH, TEST_QUERY_DB_PATH)

    def setUp(self):
        if os.path.exists(TEST_USER_DB_PATH):
            os.remove(TEST_USER_DB_PATH)
        with self.app.app_context():
            db.create_all(bind=BIND_USERS)

    def get_valid_auth_token(self):
        fake_user = User('test@test.com', 'password', 'username')
        return user_service.encode_auth_token(fake_user).decode()

    def get_expired_auth_token(self):
        return jwt.encode(
            payload={
                'exp': datetime.utcnow() - timedelta(days=1),
                'iat': datetime.utcnow() - timedelta(days=2),
                'sub': 'userid'
            },
            key=config_service.get_app_key(),
            algorithm='HS256'
        ).decode()

    def register_user(self, email, password, username):
        return self.client.post(
            API_USER_REGISTER,
            data=json.dumps(dict(
                email=email,
                password=password,
                username=username
            )),
            content_type='application/json',
        )

    def login_user(self, email, password):
        return self.client.post(
            API_USER_LOGIN,
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type='application/json',
        )

    def test_register_user(self):
        response = self.register_user('test@user.com', 'password', 'testuser')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertTrue(data['auth_token'])
        self.assertTrue(data['message'] == 'Successfully registered.')

        with self.app.app_context():
            self.assertEqual(User.query.filter(User.username == 'testuser').count(), 1)

    def test_register_user_existing_email(self):
        self.register_user('test@user.com', 'password', 'testuser')
        response = self.register_user('test@user.com', 'password2', 'testuser2')
        self.assert400(response, UserEmailExistsException.message)

    def test_register_user_existing_username(self):
        self.register_user('test@user.com', 'password', 'testuser')
        response = self.register_user('test2@user.com', 'password2', 'testuser')
        self.assert400(response, UserNameExistsException.message)

    def test_register_user_invalid_email(self):
        response = self.register_user('malformed_email', 'password', 'testuser')
        self.assert400(response, EmailNotValidException.message)

    def test_register_user_invalid_username(self):
        response = self.register_user('test@test.com', 'password', '')
        self.assert400(response, UserNameInvalidException.message)

    def test_register_user_invalid_password(self):
        response = self.register_user('test@test.com', '', 'testuser')
        self.assert400(response, PasswordInvalidException.message)


    def test_register_admin_user(self):
        with self.app.app_context():
            user_service.register_user('test@user.com', 'password', 'admin_user', True)
            self.assertTrue(db.session.query(User).filter(User.username == 'admin_user').all()[
                                0].admin)

    def test_encode_auth_token(self):
        with self.app.app_context():
            user = User(
                email='test@test.com',
                password='test',
                username='user'
            )
            db.session.add(user)
            db.session.commit()
            auth_token = user_service.encode_auth_token(user)
            self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        with self.app.app_context():
            user = User(
                email='test@test.com',
                password='test',
                username='user'
            )
            db.session.add(user)
            db.session.commit()
            auth_token = user_service.encode_auth_token(user)
            self.assertTrue(isinstance(auth_token, bytes))
            self.assertTrue(user_service.decode_auth_token(auth_token) == 1)

    def test_login_user_successful(self):
        with self.app.app_context():
            email = 'test@test.com'
            password = 'password'
            username = 'user'
            user = User(
                email=email,
                password=password,
                username=username
            )
            db.session.add(user)
            db.session.commit()

        response = self.login_user(email, password)
        self.assert200(response)
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['auth_token'])

    def test_login_unkown_user(self):
        response = self.login_user("email@email.com", "password")
        self.assert400(response)

    def test_login_wrong_password(self):
        with self.app.app_context():
            user = User(
                email="test@test.com",
                password="password",
                username="username"
            )
            db.session.add(user)
            db.session.commit()

        response = self.login_user("test@test.com", "wrong_password")
        self.assert400(response)

    def test_protected_route_logged_in(self):
        app_main.api.add_resource(ProtectedTestRoute, ProtectedTestRoute.url)
        response = self.client.get(ProtectedTestRoute.url,
                                   headers=dict(
                                       Authorization='Bearer ' +
                                                     self.get_valid_auth_token()
                                   ))
        self.assert200(response)

    def test_protected_route_not_logged_in(self):
        app_main.api.add_resource(ProtectedTestRoute, ProtectedTestRoute.url)
        response = self.client.get(ProtectedTestRoute.url)
        self.assert401(response, UnauthorizedException.message)

    def test_protected_route_token_expired(self):
        app_main.api.add_resource(ProtectedTestRoute, ProtectedTestRoute.url)
        response = self.client.get(ProtectedTestRoute.url,
                                   headers=dict(
                                       Authorization='Bearer ' +
                                                     self.get_expired_auth_token()
                                   ))
        self.assert401(response, UnauthorizedException.message)
