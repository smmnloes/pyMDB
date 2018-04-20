from flask import request
from flask_restful import Resource

from DatabaseServices import QueryService


class MovieQuery(Resource):
    def post(self):
        return QueryService.get_movies_by_criteria(request.json)


class NrOfResults(Resource):
    def post(self):
        return QueryService.get_number_results(request.json)
