import logging

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from api.movies.errors import movie_api_errors
from api.user.errors import user_api_errors
from constants.constants import BIND_USERS, BIND_MOVIES
from constants.urls import *
from services.config import config_service

db = SQLAlchemy()
cache = None
logger = None
pymdb_app = None
bcrypt = None


def create_app():
    new_app = Flask(__name__)
    init_app_config(new_app)
    db.init_app(new_app)
    init_app_logger(new_app)
    init_app_cache(new_app)
    init_app_api(new_app)
    init_bcrypt(new_app)
    global pymdb_app
    pymdb_app = new_app
    return new_app


def init_bcrypt(new_app):
    global bcrypt
    bcrypt = Bcrypt(new_app)


def init_app_api(app):
    all_api_errors = movie_api_errors
    all_api_errors.update(user_api_errors)
    api = Api(app, errors=all_api_errors)
    CORS(app, resources={"/query": {'methods': ['POST']}})
    from api.movies.controllers import MovieQuery, ResultCount, MovieByTid, TmdbDetailedData, HasDetails
    api.add_resource(MovieQuery, API_MOVIES_QUERY)
    api.add_resource(ResultCount, API_MOVIES_RESULT_COUNT)
    api.add_resource(MovieByTid, API_MOVIES_BY_TID)
    api.add_resource(TmdbDetailedData, API_MOVIES_DETAILS)
    api.add_resource(HasDetails, API_MOVIES_HAS_DETAILS)

    from api.user.controllers import Login, Logout, Register, UserInfo
    api.add_resource(Register, API_USER_REGISTER)
    api.add_resource(Login, API_USER_LOGIN)
    api.add_resource(Logout, API_USER_LOGOUT)
    api.add_resource(UserInfo, API_USER_INFO)


def init_app_cache(app):
    global cache
    cache = Cache(app, config={'CACHE_TYPE': 'simple',
                               'CACHE_DEFAULT_TIMEOUT': 0})


def init_app_logger(app):
    global logger
    logger = app.logger
    logger.setLevel(logging.INFO)


def init_app_config(app):
    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_BINDS={
            BIND_USERS: 'sqlite:///' + config_service.get_user_db_path(),
            BIND_MOVIES: 'sqlite:///' + config_service.get_movie_db_path()
        },
    )
