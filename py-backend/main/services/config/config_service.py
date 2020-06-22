import configparser
import os
import pathlib

from constants.constants import CONFIG_FILE_NAME, CONFIG_SECTION_PATHS, CONFIG_FIELD_DB_DATA, CONFIG_FIELD_TMP_DIR, \
    CONFIG_SECTION_FILE_NAMES, CONFIG_FIELD_MOVIE_DB, DB_LAST_VERSION_SUFFIX, CONFIG_SECTION_URLS, \
    CONFIG_FIELD_IMDB_URL, \
    CONFIG_SECTION_SECRETS, CONFIG_FIELD_TMDB_API_KEY, CONFIG_FIELD_USER_DB, CONFIG_FIELD_APP_KEY

config_parser = None


def init_config():
    global config_parser
    if config_parser is None:
        config_parser = configparser.ConfigParser()
        config_file_path = os.path.join(pathlib.Path(__file__).parent.absolute(), CONFIG_FILE_NAME)
        config_parser.read(config_file_path)


def init_config_decorator(func):
    def wrapper():
        init_config()
        return func()

    return wrapper


@init_config_decorator
def get_temp_path():
    return config_parser[CONFIG_SECTION_PATHS][CONFIG_FIELD_TMP_DIR]


@init_config_decorator
def get_movie_db_path():
    return os.path.join(config_parser[CONFIG_SECTION_PATHS][CONFIG_FIELD_DB_DATA],
                        config_parser[CONFIG_SECTION_FILE_NAMES][
                            CONFIG_FIELD_MOVIE_DB])


@init_config_decorator
def get_user_db_path():
    return os.path.join(config_parser[CONFIG_SECTION_PATHS][CONFIG_FIELD_DB_DATA],
                        config_parser[CONFIG_SECTION_FILE_NAMES][
                            CONFIG_FIELD_USER_DB])


@init_config_decorator
def get_last_version_path():
    return get_movie_db_path() + DB_LAST_VERSION_SUFFIX


@init_config_decorator
def get_imdb_url():
    return config_parser[CONFIG_SECTION_URLS][CONFIG_FIELD_IMDB_URL]


@init_config_decorator
def get_tmdb_api_key():
    return config_parser[CONFIG_SECTION_SECRETS][CONFIG_FIELD_TMDB_API_KEY]


@init_config_decorator
def get_app_key():
    return config_parser[CONFIG_SECTION_SECRETS][CONFIG_FIELD_APP_KEY]
