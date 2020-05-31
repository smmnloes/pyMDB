import gzip
import os
import shutil
import urllib.request

from app import app_main
from services.config import config_service
from services.database.update_service import DATASET_BASICS, DATASET_NAMES, DATASET_CREW, DATASET_PRINCIPALS, \
    DATASET_RATINGS, DATASET_AKAS

DATASETS_TO_FILENAMES = {DATASET_BASICS: 'title.basics.tsv.gz', DATASET_NAMES: 'name.basics.tsv.gz',
                         DATASET_CREW: 'title.crew.tsv.gz', DATASET_PRINCIPALS: 'title.principals.tsv.gz',
                         DATASET_RATINGS: 'title.ratings.tsv.gz', DATASET_AKAS: 'title.akas.tsv.gz'}


def download_dataset(dataset, zipped_path):
    app_main.logger.info('Downloading {} data.'.format(dataset))
    dataset_url = config_service.get_imdb_url() + DATASETS_TO_FILENAMES.get(dataset)
    urllib.request.urlretrieve(dataset_url, zipped_path)


def unzip_dataset(dataset, zipped_path, unzipped_path):
    app_main.logger.info('Unzipping {} data'.format(dataset))
    with gzip.open(zipped_path) as zipped_file:
        with open(unzipped_path, 'wb') as unzipped_file:
            shutil.copyfileobj(zipped_file, unzipped_file)


def download_and_unzip_datasets(dataset):
    temp_path = config_service.get_temp_path()
    unzipped_path = os.path.join(temp_path, dataset)
    zipped_path = unzipped_path + '_zipped'
    download_dataset(dataset, zipped_path)
    unzip_dataset(dataset, zipped_path, unzipped_path)
    os.remove(zipped_path)


def delete_downloaded_dataset(dataset):
    app_main.logger.info('Deleting local {} file'.format(dataset))
    os.remove(os.path.join(config_service.get_temp_path(), dataset))
