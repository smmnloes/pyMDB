from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base

from DatabaseServices import QueryService
from DatabaseServices.Paths import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + LOCAL_DB
db = SQLAlchemy(app)

metadata = MetaData()
metadata.reflect(db.engine)
Base = automap_base(metadata=metadata)
Base.prepare()
Base.query = db.session.query_property()

Basics = Base.classes.basics
query = db.session.query(Basics)
query = query.add_columns(Basics.primaryTitle, Basics.runtimeMinutes)
query = query.filter(Basics.primaryTitle == 'Miss Jerry')
result = query.all()
print(result)

api = Api(app)
cors = CORS(app, resources={r"/query": {"origins": "*"}})


class MovieQuery(Resource):
    def post(self):
        print("Request: {}".format(request.json))
        result = QueryService.get_movies_by_criteria(request.json)
        print("Response: {}".format(result))
        return result


api.add_resource(MovieQuery, '/query')


def start_app():
    app.run(port=5002)
