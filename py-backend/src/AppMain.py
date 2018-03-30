from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from DatabaseServices import QueryService
from definitions import *


class MovieQuery(Resource):
    def post(self):
        print("Request: {}".format(request.json))
        result = QueryService.get_movies_by_criteria(request.json)
        print("Response: {}".format(result))
        return result


def start_app():
    app = Flask(__name__)

    api = Api(app)
    api.add_resource(MovieQuery, '/query')

    cors = CORS(app, resources={r"/query": {"origins": "*"}})
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + LOCAL_DB
    QueryService.db = SQLAlchemy(app)
    QueryService.init_query_service()
    app.run(port=5002)
