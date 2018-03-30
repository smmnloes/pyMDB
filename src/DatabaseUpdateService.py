import bisect
import gzip
import os
import sqlite3
import urllib.request

PATH_LOCAL_DB_LAST_VERSION = "../DB_Data_Local/last_version/local.db"
ROOT_DB_DATA_REMOTE = "../DB_Data_Remote/"
PATH_LOCAL_DB = "../DB_Data_Local/local.db"

URL_IMDB_DATA_ROOT = "https://datasets.imdbws.com/"

DATASETS = ['basics', 'names', 'akas', 'crew', 'principals', 'ratings']
DATASETS_TO_FILENAMES = {'basics': 'title.basics.tsv.gz', 'names': 'name.basics.tsv.gz', 'akas': 'title.akas.tsv.gz',
                         'crew': 'title.crew.tsv.gz', 'principals': 'title.principals.tsv.gz',
                         'ratings': 'title.ratings.tsv.gz'}

VALID_IDS = []


def update_db():
    backup_local_db()

    try:
        for dataset in DATASETS:
            print('\nProcessing %s data.' % dataset)
            download_new_data(dataset)
            DATASETS_TO_READ_FUNCTIONS.get(dataset)()
            delete_downloaded_remote_data(dataset)
            print('Finished processing %s data.\n' % dataset)

    except Exception as e:
        print("Error while updating: {}".format(e))
        restore_db_last_version()


def backup_local_db():
    print('Backing up last version.')
    if os.path.isfile(PATH_LOCAL_DB):
        os.rename(PATH_LOCAL_DB, PATH_LOCAL_DB_LAST_VERSION)
    else:
        print('No database found, nothing to back up.')


def delete_downloaded_remote_data(dataset):
    print('Deleting local %s file' % dataset)
    os.remove(ROOT_DB_DATA_REMOTE + dataset)


def restore_db_last_version():
    print('Restoring last version.')
    if os.path.isfile(PATH_LOCAL_DB_LAST_VERSION):
        os.rename(PATH_LOCAL_DB_LAST_VERSION, PATH_LOCAL_DB)
    else:
        print("No previous version found! Cannot restore last version!")


def download_new_data(dataset):
    unzipped_path = ROOT_DB_DATA_REMOTE + dataset
    zipped_path = unzipped_path + '_zipped'
    print('Downloading %s data.' % dataset)
    urllib.request.urlretrieve(URL_IMDB_DATA_ROOT + DATASETS_TO_FILENAMES.get(dataset),
                               zipped_path)

    print('Unzipping %s data' % dataset)
    with gzip.open(zipped_path) as zipped_file:
        with open(unzipped_path, 'wb') as unzipped_file:
            unzipped_file.write(zipped_file.read())

    os.remove(zipped_path)


def is_valid_tid(to_check):
    i = bisect.bisect_left(VALID_IDS, to_check)
    if i != len(VALID_IDS) and VALID_IDS[i] == to_check:
        return True
    else:
        return False


def one_is_valid_tid(to_check):
    for x in to_check:
        if is_valid_tid(x):
            return True
    return False


def tid_to_int(imdb_id):
    return int(imdb_id[2:])


def read_basics():
    print('Reading basics to database.')
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE basics(tid TEXT PRIMARY KEY, primaryTitle TEXT, originalTitle TEXT, "
              "year INTEGER, runtimeMinutes INTEGER, genres TEXT)")

    with open(ROOT_DB_DATA_REMOTE + 'basics', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')

            if (entries[1] == "movie") & (entries[4] == "0"):
                del entries[1]
                del entries[3]
                del entries[4]
                c.execute("INSERT INTO basics VALUES (?,?,?,?,?,?)", entries)
                VALID_IDS.append(tid_to_int(entries[0]))

            line = file.readline().strip()

    conn.commit()
    conn.close()


def read_ratings():
    print('Reading ratings to database.')
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE ratings(tid TEXT PRIMARY KEY, averageRating REAL, numVotes INTEGER)")
    with open(ROOT_DB_DATA_REMOTE + 'ratings', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            if is_valid_tid(tid_to_int(entries[0])):
                c.execute("INSERT INTO ratings VALUES (?,?,?)", entries)

            line = file.readline().strip()

    conn.commit()
    conn.close()


def read_akas():
    print('Reading akas to database.')
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE akas(tid TEXT, title TEXT)")
    with open(ROOT_DB_DATA_REMOTE + 'akas', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        last_valid_id = -1
        while line:
            entries = line.split('\t')
            current_id = tid_to_int(entries[0])
            if (current_id == last_valid_id) or is_valid_tid(current_id):
                last_valid_id = current_id
                entries = entries[0:1] + entries[2:3]
                c.execute("INSERT INTO akas VALUES (?,?)", entries)

            line = file.readline().strip()

    conn.commit()
    conn.close()


def read_principals():
    print('Reading principals to database.')
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE principals(tid TEXT, nid TEXT, category TEXT, characters TEXT)")
    with open(ROOT_DB_DATA_REMOTE + 'principals', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        last_valid_id = -1
        while line:
            entries = line.split('\t')
            current_id = tid_to_int(entries[0])
            if (current_id == last_valid_id) or is_valid_tid(current_id):
                last_valid_id = current_id
                entries = entries[0:1] + entries[2:4] + entries[5:]
                c.execute("INSERT INTO principals VALUES (?,?,?,?)", entries)

            line = file.readline().strip()

    conn.commit()
    conn.close()


def read_crew():
    print('Reading crew to database.')
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE crew(tid TEXT, directors TEXT, writers TEXT)")
    with open(ROOT_DB_DATA_REMOTE + 'crew', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            if is_valid_tid(tid_to_int(entries[0])):
                c.execute("INSERT INTO crew VALUES (?,?,?)", entries)

            line = file.readline().strip()

    conn.commit()
    conn.close()


def read_names():
    print('Reading names to database.')
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE names(nid TEXT, name TEXT)")
    with open(ROOT_DB_DATA_REMOTE + 'names', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')

            if entries[5] != '\\N':
                known_for = entries[5].split(',')
                known_for = [tid_to_int(x) for x in known_for]

                if one_is_valid_tid(known_for):
                    entries = entries[0:2]
                    c.execute("INSERT INTO names VALUES (?,?)", entries)

            line = file.readline().strip()

    conn.commit()
    conn.close()


DATASETS_TO_READ_FUNCTIONS = {'basics': read_basics, 'names': read_names, 'akas': read_akas,
                              'crew': read_crew, 'principals': read_principals,
                              'ratings': read_ratings}
