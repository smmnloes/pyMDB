from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from App.RESTControllers import MovieQuery
from DatabaseServices import QueryService
from definitions import *


def start_app():
    app = Flask(__name__)

    api = Api(app)
    api.add_resource(MovieQuery, '/query')

    CORS(app, resources={r"/query": {"origins": "*"}})
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + LOCAL_DB
    QueryService.db = SQLAlchemy(app)
    QueryService.init_query_service()
    app.run(port=5002)
