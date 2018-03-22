from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource

from DatabaseServices import QueryService

app = Flask(__name__)
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
