import os

from app import app_main
from services.config import config_service


def backup_local_db():
    app_main.logger.info('Backing up last version.')
    current_db_path = config_service.get_movie_db_path()
    last_version_path = config_service.get_last_version_path()

    if os.path.isfile(current_db_path):
        os.rename(current_db_path, last_version_path)
    else:
        app_main.logger.warn('No database found, nothing to back up.')


def restore_db_last_version():
    app_main.logger.info('Restoring last version.')
    current_db_path = config_service.get_movie_db_path()
    last_version_path = config_service.get_last_version_path()

    if os.path.isfile(last_version_path):
        os.rename(last_version_path, current_db_path)
        app_main.logger.info('Last version restored!')
    else:
        app_main.logger.warn("No previous version found! Cannot restore last version!")
