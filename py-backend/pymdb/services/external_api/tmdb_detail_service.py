from urllib.parse import urljoin

import requests

from services.config import config_service

TMDB_ROOT = "https://api.themoviedb.org/3/"
TMDB_FIND_API = urljoin(TMDB_ROOT, 'find/')
TMDB_MOVIE_API = urljoin(TMDB_ROOT, 'movie/')
TMDB_CONFIG_API = urljoin(TMDB_ROOT, 'configuration')

IMAGE_BASE_PATH = None


def get_image_base_path():
    global IMAGE_BASE_PATH
    if IMAGE_BASE_PATH is None:
        params = {'api_key': config_service.get_tmdb_api_key()}
        IMAGE_BASE_PATH = requests.get(TMDB_CONFIG_API, params).json()['images']['secure_base_url']
    return IMAGE_BASE_PATH


def has_details(imdb_id):
    imdb_id_formatted = format_imdb_id(imdb_id)
    tmdb_id = get_tmdb_id(imdb_id_formatted)
    return tmdb_id is not None


def get_detailed_data_by_imdb_id(imdb_id):
    imdb_id_formatted = format_imdb_id(imdb_id)
    tmdb_id = get_tmdb_id(imdb_id_formatted)
    if tmdb_id is None:
        return None

    return get_details_for_tmdb_id(tmdb_id)


def get_tmdb_id(imdb_id_formatted):
    params = {'api_key': config_service.get_tmdb_api_key(), 'external_source': 'imdb_id'}
    url = urljoin(TMDB_FIND_API, imdb_id_formatted)
    response = requests.get(url, params)
    response_json = response.json()
    if len(response_json['movie_results']) > 0:
        return response_json['movie_results'][0]['id']
    return None


# Poster sizes:
# "w92",
# "w154",
# "w185",
# "w342",
# "w500",
# "w780",
# "original"

def get_details_for_tmdb_id(tmdb_id):
    params = {'api_key': config_service.get_tmdb_api_key(), 'append_to_response': 'credits'}
    url = urljoin(TMDB_MOVIE_API, str(tmdb_id))
    response = requests.get(url, params).json()
    poster_path = response['poster_path']
    if poster_path is not None:
        response['poster_path'] = get_image_base_path() + 'w342' + poster_path
    return response


def format_imdb_id(input_id):
    while len(input_id) < 7:
        input_id = "0" + input_id
    return "tt" + input_id
