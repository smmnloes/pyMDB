from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from definitions import *

db = SQLAlchemy()


def start_app():
    app = create_app()
    app.run(port=5002)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + LOCAL_DB
    CORS(app, resources={r"/query": {'methods': ['POST']}})
    db.init_app(app)
    api = Api(app)

    from App.RESTControllers import MovieQuery
    api.add_resource(MovieQuery, '/query')
    return app
