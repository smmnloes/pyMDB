from flask import request
from flask_restful import Resource

from App.ApiErrors import DetailedDataNotFound, NoTmdbApiKeySpecified
from Config import ConfigService
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
        if not ConfigService.get_tmdb_api_key():
            raise NoTmdbApiKeySpecified
        detailed_data = TMDBDetailService.get_detailed_data_by_imdb_id(request.args.get('imdbid'))
        if detailed_data is None:
            raise DetailedDataNotFound
        return detailed_data
