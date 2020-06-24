from app import app_main
from constants.constants import BIND_USERS, BIND_MOVIES


def create_test_app(user_db_path, movie_db_path):
    test_app = app_main.create_app()
    test_app.config.update(
        SQLALCHEMY_BINDS={
            BIND_USERS: 'sqlite:///' + user_db_path,
            BIND_MOVIES: 'sqlite:///' + movie_db_path
        }
    )
    return test_app
