from flask import Flask

from constants.constants import BIND_USERS, BIND_MOVIES


def create_test_app(user_db_path, movie_db_path):
    test_app = Flask(__name__)
    test_app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_BINDS={
            BIND_USERS: 'sqlite:///' + user_db_path,
            BIND_MOVIES: 'sqlite:///' + movie_db_path
        }
    )
    return test_app
