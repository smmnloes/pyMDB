from flask import request
from flask_restful import Resource

from Services.API import TMDBDetailService
from Services.Database import QueryService


class MovieQuery(Resource):
    def post(self):
        return QueryService.get_movies_by_criteria(request.json)


class ResultCount(Resource):
    def post(self):
        return QueryService.get_number_results(request.json)


class MovieByTid(Resource):
    def post(self):
        return QueryService.get_movie_by_tid(request.json)


class TmdbDetailedData(Resource):
    def get(self):
        return TMDBDetailService.get_detailed_data_by_imdb_id(request.json)