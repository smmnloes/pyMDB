import gzip
import os
import sqlite3
import urllib.request

PATH_LOCAL_DB_LAST_VERSION = "../DB_Data_Local/last_version/local.db"
ROOT_DB_DATA_REMOTE = "../DB_Data_Remote/"
PATH_LOCAL_DB = "../DB_Data_Local/local.db"

URL_IMDB_DATA_ROOT = "https://datasets.imdbws.com/"

DATASETS_TO_FILENAMES = {'basics': 'title.basics.tsv.gz', 'names': 'name.basics.tsv.gz', 'akas': 'title.akas.tsv.gz',
                         'crew': 'title.crew.tsv.gz', 'principals': 'title.principals.tsv.gz',
                         'ratings': 'title.ratings.tsv.gz'}


def update_db():
    backup_last_version()

    try:
        for dataset in DATASETS_TO_FILENAMES:
            download_new_data(dataset)
    except Exception as e:
        print("Error while updating: {}\nRestoring last dabase version!".format(e))
        restore_last_version()


def backup_last_version():
    print('Backing up last version!')
    if os.path.isfile(PATH_LOCAL_DB):
        os.rename(PATH_LOCAL_DB, PATH_LOCAL_DB_LAST_VERSION)
    else:
        print('No database found, nothing to back up.')


def restore_last_version():
    if os.path.isfile(PATH_LOCAL_DB_LAST_VERSION):
        os.rename(PATH_LOCAL_DB_LAST_VERSION, PATH_LOCAL_DB)
    else:
        print("No previous version found! Sorry...")


def download_new_data(dataset):
    unzipped_path = ROOT_DB_DATA_REMOTE + dataset
    zipped_path = unzipped_path + '_zipped'
    print('Downloading %s data' % dataset)
    urllib.request.urlretrieve(URL_IMDB_DATA_ROOT + DATASETS_TO_FILENAMES.get(dataset),
                               zipped_path)

    print('Unzipping %s data' % dataset)
    with gzip.open(zipped_path) as zipped_file:
        with open(unzipped_path, 'wb') as unzipped_file:
            unzipped_file.write(zipped_file.read())

    os.remove(zipped_path)
    print('Finished processing %s data' % dataset)


def read_title_basisc():
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS {}(tconst TEXT PRIMARY KEY , primaryTitle TEXT, originalTitle TEXT, "
              "year INTEGER, runtimeMinutes INTEGER, genres TEXT)".format('basics'))

    with open(ROOT_DB_DATA_REMOTE + 'basics', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        count = 1
        while line:
            entries = line.split('\t')

            if (entries[1] == "movie") & (entries[4] == "0"):
                del entries[1]
                del entries[3]
                del entries[4]
                c.execute("INSERT OR REPlACE INTO {} VALUES (?,?,?,?,?,?)".format('basics'), entries)

            line = file.readline().strip()
            print("Reading line %d" % count)
            count += 1

    conn.commit()
    conn.close()
