import bisect
import gzip
import os
import sqlite3
import urllib.request

import definitions
from App.AppMain import db, create_app

# DATASETS = ['basics']
DATASETS = ['basics', 'names', 'crew', 'principals', 'ratings']
DATASETS_TO_FILENAMES = {'basics': 'title.basics.tsv.gz', 'names': 'name.basics.tsv.gz',
                         'crew': 'title.crew.tsv.gz', 'principals': 'title.principals.tsv.gz',
                         'ratings': 'title.ratings.tsv.gz'}

VALID_IDS = []

app = create_app()


def update_db():
    backup_local_db()

    with app.app_context():
        db.create_all()

    try:
        for dataset in DATASETS:
            print('\nProcessing {} data.'.format(dataset))
            # download_new_data(dataset)
            print('Reading {} to database.'.format(dataset))
            DATASETS_TO_READ_FUNCTIONS.get(dataset)()
            # delete_downloaded_remote_data(dataset)
            print('Finished processing {} data.\n'.format(dataset))

    except (Exception, BaseException) as e:
        print("Error while updating: {}".format(e))
        restore_db_last_version()

    analyze()


def get_db_connect():
    db_connect = sqlite3.connect(definitions.LOCAL_DB)
    db_connect.execute("PRAGMA synchronous = 0")
    return db_connect


def backup_local_db():
    print('Backing up last version.')
    if os.path.isfile(definitions.LOCAL_DB):
        os.rename(definitions.LOCAL_DB, definitions.DB_LAST_VERSION)
    else:
        print('No database found, nothing to back up.')


def delete_downloaded_remote_data(dataset):
    print('Deleting local {} file'.format(dataset))
    os.remove(definitions.DB_DATA_REMOTE + dataset)


def restore_db_last_version():
    print('Restoring last version.')
    if os.path.isfile(definitions.DB_LAST_VERSION):
        os.rename(definitions.DB_LAST_VERSION, definitions.LOCAL_DB)
    else:
        print("No previous version found! Cannot restore last version!")


def download_new_data(dataset):
    unzipped_path = definitions.DB_DATA_REMOTE + dataset
    zipped_path = unzipped_path + '_zipped'
    print('Downloading {} data.'.format(dataset))
    urllib.request.urlretrieve(definitions.URL_IMDB_DATA + DATASETS_TO_FILENAMES.get(dataset),
                               zipped_path)

    print('Unzipping {} data'.format(dataset))
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


def analyze():
    db_connect = sqlite3.connect(definitions.LOCAL_DB)
    db_connect.execute('ANALYZE')


def read_basics():
    db_connect = get_db_connect()

    with open(definitions.DB_DATA_REMOTE + 'basics', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')

            if (entries[1] == "movie") & (entries[4] == "0"):
                entries_basics = clean_nulls(entries[0:1] + entries[2:3] + entries[5:6] + entries[7:8])
                genres = entries[8]
                db_connect.execute("INSERT INTO basics VALUES (?,?,?,?)", entries_basics)
                if genres != '\\N':
                    for genre in genres.split(','):
                        db_connect.execute("INSERT INTO genres VALUES (?,?)", (entries[0], genre))
                VALID_IDS.append(tid_to_int(entries[0]))

            line = file.readline().strip()

        db_connect.commit()
        db_connect.close()


def read_ratings():
    db_connect = get_db_connect()

    with open(definitions.DB_DATA_REMOTE + 'ratings', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            if is_valid_tid(tid_to_int(entries[0])):
                db_connect.execute("INSERT INTO ratings VALUES (?,?,?)", entries)

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def read_principals():
    db_connect = get_db_connect()

    with open(definitions.DB_DATA_REMOTE + 'principals', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        rowid = 0
        last_valid_id = -1
        while line:
            entries = line.split('\t')
            current_id = tid_to_int(entries[0])
            if (current_id == last_valid_id) or is_valid_tid(current_id):
                last_valid_id = current_id
                entries = clean_nulls(entries[0:1] + entries[2:4] + entries[5:])
                db_connect.execute("INSERT OR REPLACE INTO principals VALUES (?,?,?,?,?)", [rowid] + entries)
                rowid += 1

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def read_crew():
    db_connect = get_db_connect()

    with open(definitions.DB_DATA_REMOTE + 'crew', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            if is_valid_tid(tid_to_int(entries[0])):
                if entries[1] != '\\N':
                    for director in entries[1].split(','):
                        db_connect.execute("INSERT INTO directors VALUES (?,?)", (entries[0], director))

                if entries[2] != '\\N':
                    for writer in entries[2].split(','):
                        db_connect.execute("INSERT INTO writers VALUES (?,?)", (entries[0], writer))

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def read_names():
    db_connect = get_db_connect()

    with open(definitions.DB_DATA_REMOTE + 'names', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')

            if entries[5] != '\\N':
                known_for = entries[5].split(',')
                known_for = [tid_to_int(x) for x in known_for]

                if one_is_valid_tid(known_for):
                    entries = entries[0:2]
                    db_connect.execute("INSERT INTO names VALUES (?,?)", entries)

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def clean_nulls(entries):
    return [None if entry == '\\N' else entry for entry in entries]


DATASETS_TO_READ_FUNCTIONS = {'basics': read_basics, 'names': read_names,
                              'crew': read_crew, 'principals': read_principals,
                              'ratings': read_ratings}
