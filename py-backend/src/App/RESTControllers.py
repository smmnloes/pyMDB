from flask import request
from flask_restful import Resource

from DatabaseServices import QueryService


class MovieQuery(Resource):
    def post(self):
        return QueryService.get_movies_by_criteria(request.json)


class ResultCount(Resource):
    def post(self):
        return QueryService.get_number_results(request.json)


class MovieByTid(Resource):
    def post(self):
        return QueryService.get_movie_by_tid(request.json)
