import logging
from urllib.parse import urljoin

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from App.ApiErrors import rest_api_errors
from Config import ConfigService

db = SQLAlchemy()
API_ROOT = '/api/'


def start_app():
    app = create_app()
    app.run(port=5002)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + ConfigService.get_movie_db_path()
    CORS(app, resources={"/query": {'methods': ['POST']}})
    db.init_app(app)
    api = Api(app, errors=rest_api_errors)
    app.logger.setLevel(logging.INFO)

    from App.RESTControllers import MovieQuery, ResultCount, MovieByTid, TmdbDetailedData, HasDetails
    api.add_resource(MovieQuery, urljoin(API_ROOT, 'query'))
    api.add_resource(ResultCount, urljoin(API_ROOT, 'result_count'))
    api.add_resource(MovieByTid, urljoin(API_ROOT, 'movie_by_tid'))
    api.add_resource(TmdbDetailedData, urljoin(API_ROOT, 'details'))
    api.add_resource(HasDetails, urljoin(API_ROOT, 'has_details'))

    return app
