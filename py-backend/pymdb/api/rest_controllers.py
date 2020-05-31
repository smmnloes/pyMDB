import hashlib
import json

from flask import request
from flask_restful import Resource

from api.api_errors import DetailedDataNotFound, NoTmdbApiKeySpecified
from app import app_main
from services.config import config_service
from services.database import query_service
from services.external_api import tmdb_detail_service


def make_post_cache_key():
    body_json_dump = json.dumps(request.json, sort_keys=True)
    path_and_dump = request.path + body_json_dump
    return hashlib.md5(path_and_dump.encode('utf-8')).hexdigest()


def require_tmdb_api_key(fun):
    def wrapper(*args, **kwargs):
        if not config_service.get_tmdb_api_key():
            raise NoTmdbApiKeySpecified
        return fun(*args, **kwargs)

    return wrapper


class MovieQuery(Resource):
    @app_main.cache.cached(key_prefix=make_post_cache_key)
    def post(self):
        return query_service.get_movies_by_criteria(request.json)


class ResultCount(Resource):
    @app_main.cache.cached(key_prefix=make_post_cache_key)
    def post(self):
        return query_service.get_result_count_by_criteria(request.json)


class MovieByTid(Resource):
    @app_main.cache.cached(key_prefix=make_post_cache_key)
    def post(self):
        return query_service.get_movie_by_tid(request.json)


class HasDetails(Resource):
    @require_tmdb_api_key
    @app_main.cache.cached(query_string=True)
    def get(self):
        return tmdb_detail_service.has_details(request.args.get('imdbid'))


class TmdbDetailedData(Resource):
    @require_tmdb_api_key
    @app_main.cache.cached(query_string=True)
    def get(self):
        detailed_data = tmdb_detail_service.get_detailed_data_by_imdb_id(request.args.get('imdbid'))
        if detailed_data is None:
            raise DetailedDataNotFound
        return detailed_data
