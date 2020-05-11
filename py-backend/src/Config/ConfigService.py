import configparser
import os
import pathlib

CONFIG_FILE_NAME = "config.ini"
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
    return config_parser['PATHS']['temp']


@init_config_decorator
def get_movie_db_path():
    return os.path.join(config_parser['PATHS']['db_data'], config_parser['FILE_NAMES']['movie_db'])


@init_config_decorator
def get_last_version_path():
    return get_movie_db_path() + '_last_version'


@init_config_decorator
def get_imdb_url():
    return config_parser['URLS']['IMDB_DATA']
