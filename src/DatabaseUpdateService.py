import gzip
import os
import sqlite3
import urllib.request

PATH_LOCAL_DB_LAST_VERSION = "../DB_Data_Local/last_version/local.db"
ROOT_DB_DATA_REMOTE = "../DB_Data_Remote/"
PATH_LOCAL_DB = "../DB_Data_Local/local.db"

TITLE_BASICS = "basics"

URL_IMDB_DATA_ROOT = "https://datasets.imdbws.com/"

DATASETS_TO_FILENAMES = {'basics': 'title.basics.tsv.gz', 'names': 'name.basics.tsv.gz', 'akas': 'title.akas.tsv.gz',
                         'crew': 'title.crew.tsv.gz', 'principals': 'title.principals.tsv.gz',
                         'ratings': 'title.ratings.tsv.gz'}


class DatabaseUpdateService:
    def update_db(self):
        self.backup_last_version()

        try:
            for dataset in DATASETS_TO_FILENAMES:
                self.download_new_data(dataset)
        except Exception:
            self.restore_last_version()

    def backup_last_version(self):
        if os.path.isfile(PATH_LOCAL_DB):
            os.rename(PATH_LOCAL_DB, PATH_LOCAL_DB_LAST_VERSION)

    def restore_last_version(self):
        if os.path.isfile(PATH_LOCAL_DB_LAST_VERSION):
            os.rename(PATH_LOCAL_DB_LAST_VERSION, PATH_LOCAL_DB)
        else:
            print("No previous version found! Sorry...")

    def download_new_data(self, dataset):
        unzipped_path = ROOT_DB_DATA_REMOTE + dataset
        zipped_path = unzipped_path + '_zipped'
        urllib.request.urlretrieve(URL_IMDB_DATA_ROOT + DATASETS_TO_FILENAMES.get(dataset),
                                   zipped_path)

        with gzip.open(zipped_path) as zipped_file:
            with open(unzipped_path, 'wb') as unzipped_file:
                unzipped_file.write(zipped_file.read())

        os.remove(zipped_path)


    def read_title_basisc(self):
        conn = sqlite3.connect(PATH_LOCAL_DB)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS {}(tconst TEXT PRIMARY KEY , primaryTitle TEXT, originalTitle TEXT, "
                  "year INTEGER, runtimeMinutes INTEGER, genres TEXT)".format(TITLE_BASICS))

        with open(ROOT_DB_DATA_REMOTE + TITLE_BASICS + ".tsv", 'r') as file:
            line = file.readline()
            line = file.readline().strip()

            count = 1
            while line:
                entries = line.split('\t')

                if (entries[1] == "movie") & (entries[4] == "0"):
                    del entries[1]
                    del entries[3]
                    del entries[4]
                    c.execute("INSERT OR REPlACE INTO {} VALUES (?,?,?,?,?,?)".format(TITLE_BASICS), entries)

                line = file.readline().strip()
                print("Reading line %d" % count)
                count += 1

        conn.commit()
        conn.close()
