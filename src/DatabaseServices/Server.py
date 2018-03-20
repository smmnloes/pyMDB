from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class MovieQuery(Resource):
    def post(self):
        print(request.json)


api.add_resource(MovieQuery, '/query')


def start_app():
    app.run(port=5002)
