from flask import request
from flask_restful import Resource

from DatabaseServices import QueryService


class MovieQuery(Resource):
    def post(self):
        print("Request: {}".format(request.json))
        result = QueryService.get_movies_by_criteria(request.json)
        print("Response: {}".format(result))
        return result

