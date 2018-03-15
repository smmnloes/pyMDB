import sqlite3
import urllib.request
from pathlib import Path

PATH_DB_LAST_VERSION = "../DB_Data_Local/last_version"
ROOT_DB_DATA_REMOTE = "../DB_Data_Remote/"
PATH_LOCAL_DB = "../DB_Data_Local/local.db"

TITLE_BASICS = "basics"

URL_IMDB_DATA_ROOT = "https://datasets.imdbws.com/"


class DatabaseUpdateService:
    def update_db(self):
        self.backup_last_version()

    def backup_last_version(self):
        current_db_file = Path(PATH_LOCAL_DB)
        if current_db_file.is_file():
            current_db_file.rename(Path(PATH_DB_LAST_VERSION, current_db_file.name))

    def download_new_data(self):
        urllib.request.urlretrieve(URL_IMDB_DATA_ROOT + 'title.basics.tsv.gz', ROOT_DB_DATA_REMOTE + 'basics_zipped')

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
