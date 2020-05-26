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
        return QueryService.get_movies_by_criteria(request.json, get_count=True)


class MovieByTid(Resource):
    def post(self):
        return QueryService.get_movie_by_tid(request.json)


def require_tmdb_api_key(fun):
    def wrapper(*args, **kwargs):
        if not ConfigService.get_tmdb_api_key():
            raise NoTmdbApiKeySpecified
        return fun(*args, **kwargs)

    return wrapper


class HasDetails(Resource):
    @require_tmdb_api_key
    def get(self):
        return TMDBDetailService.has_details(request.args.get('imdbid'))


class TmdbDetailedData(Resource):
    @require_tmdb_api_key
    def get(self):
        detailed_data = TMDBDetailService.get_detailed_data_by_imdb_id(request.args.get('imdbid'))
        if detailed_data is None:
            raise DetailedDataNotFound
        return detailed_data
