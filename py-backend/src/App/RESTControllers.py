import hashlib
import json

from flask import request
from flask_restful import Resource

from App import AppMain
from App.ApiErrors import DetailedDataNotFound, NoTmdbApiKeySpecified
from Config import ConfigService
from Services.API import TMDBDetailService
from Services.Database import QueryService


def make_post_cache_key():
    body_json_dump = json.dumps(request.json, sort_keys=True)
    path_and_dump = request.path + body_json_dump
    return hashlib.md5(path_and_dump.encode('utf-8')).hexdigest()


def require_tmdb_api_key(fun):
    def wrapper(*args, **kwargs):
        if not ConfigService.get_tmdb_api_key():
            raise NoTmdbApiKeySpecified
        return fun(*args, **kwargs)

    return wrapper


class MovieQuery(Resource):
    @AppMain.cache.cached(key_prefix=make_post_cache_key)
    def post(self):
        return QueryService.get_movies_by_criteria(request.json)


class ResultCount(Resource):
    @AppMain.cache.cached(key_prefix=make_post_cache_key)
    def post(self):
        return QueryService.get_result_count_by_criteria(request.json)


class MovieByTid(Resource):
    @AppMain.cache.cached(key_prefix=make_post_cache_key)
    def post(self):
        return QueryService.get_movie_by_tid(request.json)


class HasDetails(Resource):
    @require_tmdb_api_key
    @AppMain.cache.cached(query_string=True)
    def get(self):
        return TMDBDetailService.has_details(request.args.get('imdbid'))


class TmdbDetailedData(Resource):
    @require_tmdb_api_key
    @AppMain.cache.cached(query_string=True)
    def get(self):
        detailed_data = TMDBDetailService.get_detailed_data_by_imdb_id(request.args.get('imdbid'))
        if detailed_data is None:
            raise DetailedDataNotFound
        return detailed_data
