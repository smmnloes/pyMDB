import json
import os
from unittest.mock import patch, MagicMock

from flask_testing import TestCase

from api.user.errors import UserEmailExistsException, UserNameExistsException, EmailNotValidException, \
    TokenExpiredException, NoTokenProvidedException, TokenBlacklistedException
from constants.urls import API_USER_REGISTER, API_USER_LOGIN, API_USER_LOGOUT
from model.user_model import *
from resources.resources_paths import TEST_QUERY_DB_PATH, TEST_USER_DB_PATH
from services.user import user_service
from test_utils import create_test_app, expired_auth_token


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
            auth_token = user_service.encode_auth_token(user.id)
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
            auth_token = user_service.encode_auth_token(user.id)
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

    def test_logout_user(self):
        email = "test@test.com"
        password = "password"
        username = "username"
        self.register_user(email, password, username)
        login_response = self.login_user(email, password)
        logout_response = self.client.post(
            API_USER_LOGOUT,
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    login_response.data.decode()
                )['auth_token']
            )
        )
        self.assert200(logout_response, 'Successfully logged out.')

    def test_logout_not_logged_in(self):
        logout_response = self.client.post(
            API_USER_LOGOUT,
        )
        self.assert400(logout_response, NoTokenProvidedException.message)

    def test_logout_token_expired(self):
        logout_response = self.client.post(
            API_USER_LOGOUT,
            headers=dict(
                Authorization='Bearer ' +
                              expired_auth_token.decode()
            )
        )
        self.assert400(logout_response, TokenExpiredException.message)

    def test_logout_token_blacklisted(self):
        token = user_service.encode_auth_token('fake_id').decode()
        with self.app.app_context():
            db.session.add(BlacklistToken(token))
            db.session.commit()

        logout_response = self.client.post(
            API_USER_LOGOUT,
            headers=dict(
                Authorization='Bearer ' +
                              token
            )
        )
        self.assert400(logout_response, TokenBlacklistedException.message)

    def test_get_user_info(self):
        pass

    # TODO: test on protected routes
    def test_token_expired(self):
        pass

    def test_token_blacklisted(self):
        pass
