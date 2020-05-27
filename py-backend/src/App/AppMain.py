import logging
from urllib.parse import urljoin

from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from App.ApiErrors import rest_api_errors
from Config import ConfigService

db = SQLAlchemy()
API_ROOT = '/api/'
cache = None
logger = None
pymdb_app = None


def start_app():
    create_app().run(port=5002)


def create_app():
    global pymdb_app
    pymdb_app = Flask(__name__)
    global logger
    logger = pymdb_app.logger
    pymdb_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    pymdb_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + ConfigService.get_movie_db_path()
    CORS(pymdb_app, resources={"/query": {'methods': ['POST']}})
    db.init_app(pymdb_app)
    api = Api(pymdb_app, errors=rest_api_errors)
    pymdb_app.logger.setLevel(logging.INFO)
    global cache
    cache = Cache(pymdb_app, config={'CACHE_TYPE': 'simple',
                                     "CACHE_DEFAULT_TIMEOUT": 0})

    from App.RESTControllers import MovieQuery, ResultCount, MovieByTid, TmdbDetailedData, HasDetails
    api.add_resource(MovieQuery, urljoin(API_ROOT, 'query'))
    api.add_resource(ResultCount, urljoin(API_ROOT, 'result_count'))
    api.add_resource(MovieByTid, urljoin(API_ROOT, 'movie_by_tid'))
    api.add_resource(TmdbDetailedData, urljoin(API_ROOT, 'details'))
    api.add_resource(HasDetails, urljoin(API_ROOT, 'has_details'))

    return pymdb_app
