import logging
import os
from urllib.parse import urljoin

from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from api.api_errors import rest_api_errors
from constants.constants import APP_PORT, BIND_USERS, BIND_MOVIES
from services.config import config_service

db = SQLAlchemy()
API_ROOT = '/api/'
cache = None
logger = None
pymdb_app = None


def start_app():
    create_app().run(port=APP_PORT)


def create_app():
    new_app = Flask(__name__)
    init_app_config(new_app)
    db.init_app(new_app)
    init_app_logger(new_app)
    init_app_cache(new_app)
    init_app_api(new_app)
    init_app_user_db(new_app)
    global pymdb_app
    pymdb_app = new_app
    return new_app


def init_app_user_db(app):
    if not os.path.exists(config_service.get_user_db_path()):
        with app.app_context():
            db.create_all(bind=BIND_USERS)


def init_app_api(app):
    api = Api(app, errors=rest_api_errors)
    CORS(app, resources={"/query": {'methods': ['POST']}})
    from api.rest_controllers import MovieQuery, ResultCount, MovieByTid, TmdbDetailedData, HasDetails
    api.add_resource(MovieQuery, urljoin(API_ROOT, 'query'))
    api.add_resource(ResultCount, urljoin(API_ROOT, 'result_count'))
    api.add_resource(MovieByTid, urljoin(API_ROOT, 'movie_by_tid'))
    api.add_resource(TmdbDetailedData, urljoin(API_ROOT, 'details'))
    api.add_resource(HasDetails, urljoin(API_ROOT, 'has_details'))


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
        USER_EMAIL_SENDER_EMAIL='max@pymdb.mloesch.it',
        SECRET_KEY=config_service.get_app_key()
    )
