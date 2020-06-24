from datetime import datetime, timedelta

import jwt

from app import app_main
from constants.constants import BIND_USERS, BIND_MOVIES
from services.config import config_service


def create_test_app(user_db_path, movie_db_path):
    test_app = app_main.create_app()
    test_app.config.update(
        SQLALCHEMY_BINDS={
            BIND_USERS: 'sqlite:///' + user_db_path,
            BIND_MOVIES: 'sqlite:///' + movie_db_path
        }
    )
    return test_app


expired_auth_token = jwt.encode(
    payload={
        'exp': datetime.utcnow() - timedelta(days=1),
        'iat': datetime.utcnow() - timedelta(days=2),
        'sub': 'userid'
    },
    key=config_service.get_app_key(),
    algorithm='HS256'
)
