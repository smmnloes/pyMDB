import bisect
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

VALID_IDS = []


def update_db():
    backup_last_version()

    try:
        for dataset in DATASETS_TO_FILENAMES:
            download_new_data(dataset)

        read_basics()
        read_principals()
        read_akas()
        read_ratings()
        read_crew()
        read_names()

        for dataset in DATASETS_TO_FILENAMES:
            delete_downloaded_remote_data(dataset)

    except Exception as e:
        print("Error while updating: {}\nRestoring last dabase version!".format(e))
        restore_last_version()


def backup_last_version():
    print('Backing up last version!')
    if os.path.isfile(PATH_LOCAL_DB):
        os.rename(PATH_LOCAL_DB, PATH_LOCAL_DB_LAST_VERSION)
    else:
        print('No database found, nothing to back up.')


def delete_downloaded_remote_data(dataset):
    print('Deleting local %s file' % dataset)
    os.remove(ROOT_DB_DATA_REMOTE + dataset)


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


def is_valid_id(to_check):
    i = bisect.bisect_left(VALID_IDS, to_check)
    if i != len(VALID_IDS) and VALID_IDS[i] == to_check:
        return True
    else:
        return False


def one_is_valid_id(to_check):
    for x in to_check:
        if is_valid_id(x):
            return True
    return False


def imdb_id_to_int(imdb_id):
    return int(imdb_id[2:])


def read_basics():
    print('Reading basics...')
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
                VALID_IDS.append(imdb_id_to_int(entries[0]))

            line = file.readline().strip()

    conn.commit()
    conn.close()


def read_ratings():
    print('Reading ratings...')
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE ratings(tid TEXT PRIMARY KEY, averageRating REAL, numVotes INTEGER)")
    with open(ROOT_DB_DATA_REMOTE + 'ratings', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            if is_valid_id(imdb_id_to_int(entries[0])):
                c.execute("INSERT INTO ratings VALUES (?,?,?)", entries)

            line = file.readline().strip()

    conn.commit()
    conn.close()


def read_akas():
    print('Reading akas...')
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE akas(tid TEXT, title TEXT)")
    with open(ROOT_DB_DATA_REMOTE + 'akas', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        last_valid_id = -1
        while line:
            entries = line.split('\t')
            current_id = imdb_id_to_int(entries[0])
            if (current_id == last_valid_id) or is_valid_id(current_id):
                last_valid_id = current_id
                entries = entries[0:1] + entries[2:3]
                c.execute("INSERT INTO akas VALUES (?,?)", entries)

            line = file.readline().strip()

    conn.commit()
    conn.close()


def read_principals():
    print('Reading principals...')
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE principals(tid TEXT, nid TEXT, category TEXT, characters TEXT)")
    with open(ROOT_DB_DATA_REMOTE + 'principals', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        last_valid_id = -1
        while line:
            entries = line.split('\t')
            current_id = imdb_id_to_int(entries[0])
            if (current_id == last_valid_id) or is_valid_id(current_id):
                last_valid_id = current_id
                entries = entries[0:1] + entries[2:4] + entries[5:]
                c.execute("INSERT INTO principals VALUES (?,?,?,?)", entries)

            line = file.readline().strip()

    conn.commit()
    conn.close()


def read_crew():
    print('Reading crew...')
    conn = sqlite3.connect(PATH_LOCAL_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE crew(tid TEXT, directors TEXT, writers TEXT)")
    with open(ROOT_DB_DATA_REMOTE + 'crew', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            if is_valid_id(imdb_id_to_int(entries[0])):
                c.execute("INSERT INTO crew VALUES (?,?,?)", entries)

            line = file.readline().strip()

    conn.commit()
    conn.close()


def read_names():
    print('Reading names...')
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
                known_for = [imdb_id_to_int(x) for x in known_for]

                if one_is_valid_id(known_for):
                    entries = entries[0:2]
                    c.execute("INSERT INTO names VALUES (?,?)", entries)

            line = file.readline().strip()

    conn.commit()
    conn.close()
