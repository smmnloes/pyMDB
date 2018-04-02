from flask import request
from flask_restful import Resource

from DatabaseServices import QueryService


class MovieQuery(Resource):
    def post(self):
        result = QueryService.get_movies_by_criteria(request.json)
        return result
