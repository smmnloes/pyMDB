import bisect
import gzip
import os
import sqlite3
import urllib.request

from DatabaseServices import Paths

DATASETS = ['basics', 'names', 'akas', 'crew', 'principals', 'ratings']
DATASETS_TO_FILENAMES = {'basics': 'title.basics.tsv.gz', 'names': 'name.basics.tsv.gz', 'akas': 'title.akas.tsv.gz',
                         'crew': 'title.crew.tsv.gz', 'principals': 'title.principals.tsv.gz',
                         'ratings': 'title.ratings.tsv.gz'}

VALID_IDS = []


def update_db():
    # backup_local_db()

    try:
        for dataset in DATASETS:
            print('\nProcessing %s data.' % dataset)
            # download_new_data(dataset)
            DATASETS_TO_READ_FUNCTIONS.get(dataset)()
            # delete_downloaded_remote_data(dataset)
            print('Finished processing %s data.\n' % dataset)

    except (Exception, BaseException) as e:
        print("Error while updating: {}".format(e))
        restore_db_last_version()

    analyze()


def backup_local_db():
    print('Backing up last version.')
    if os.path.isfile(Paths.LOCAL_DB):
        os.rename(Paths.LOCAL_DB, Paths.DB_LAST_VERSION)
    else:
        print('No database found, nothing to back up.')


def delete_downloaded_remote_data(dataset):
    print('Deleting local %s file' % dataset)
    os.remove(Paths.DB_DATA_REMOTE + dataset)


def restore_db_last_version():
    print('Restoring last version.')
    if os.path.isfile(Paths.DB_LAST_VERSION):
        os.rename(Paths.DB_LAST_VERSION, Paths.LOCAL_DB)
    else:
        print("No previous version found! Cannot restore last version!")


def download_new_data(dataset):
    unzipped_path = Paths.DB_DATA_REMOTE + dataset
    zipped_path = unzipped_path + '_zipped'
    print('Downloading %s data.' % dataset)
    urllib.request.urlretrieve(Paths.URL_IMDB_DATA + DATASETS_TO_FILENAMES.get(dataset),
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


def analyze():
    db_connect = sqlite3.connect(Paths.LOCAL_DB)
    db_connect.execute('ANALYZE')


def read_basics():
    print('Reading basics to database.')
    db_connect = sqlite3.connect(Paths.LOCAL_DB)
    db_connect.execute("PRAGMA synchronous = 0")
    db_connect.execute("CREATE TABLE basics(tid TEXT PRIMARY KEY, primaryTitle TEXT, "
                       "year INTEGER, runtimeMinutes INTEGER, genres TEXT)")

    with open(Paths.DB_DATA_REMOTE + 'basics', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')

            if (entries[1] == "movie") & (entries[4] == "0"):
                entries = entries[0:1] + entries[2:3] + entries[5:6] + entries[7:]
                db_connect.execute("INSERT INTO basics VALUES (?,?,?,?,?)", entries)
                VALID_IDS.append(tid_to_int(entries[0]))

            line = file.readline().strip()

        db_connect.commit()
        db_connect.close()


def read_ratings():
    print('Reading ratings to database.')
    db_connect = sqlite3.connect(Paths.LOCAL_DB)
    db_connect.execute("PRAGMA synchronous = 0")
    db_connect.execute(
        "CREATE TABLE ratings(tid TEXT PRIMARY KEY , averageRating REAL, numVotes INTEGER, "
        "FOREIGN KEY (tid) REFERENCES basics(tid))")
    with open(Paths.DB_DATA_REMOTE + 'ratings', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            if is_valid_tid(tid_to_int(entries[0])):
                db_connect.execute("INSERT INTO ratings VALUES (?,?,?)", entries)

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def read_akas():
    print('Reading akas to database.')
    db_connect = sqlite3.connect(Paths.LOCAL_DB)
    db_connect.execute("PRAGMA synchronous = 0")
    db_connect.execute("CREATE TABLE akas(tid TEXT, title TEXT, "
                       "FOREIGN KEY (tid) REFERENCES basics(tid),"
                       "PRIMARY KEY (tid,title))")
    with open(Paths.DB_DATA_REMOTE + 'akas', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        last_valid_id = -1
        while line:
            entries = line.split('\t')
            current_id = tid_to_int(entries[0])
            if (current_id == last_valid_id) or is_valid_tid(current_id):
                last_valid_id = current_id
                entries = entries[0:1] + entries[2:3]
                db_connect.execute("INSERT OR REPLACE INTO akas VALUES (?,?)", entries)

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def read_principals():
    print('Reading principals to database.')
    db_connect = sqlite3.connect(Paths.LOCAL_DB)
    db_connect.execute("PRAGMA synchronous = 0")
    db_connect.execute("CREATE TABLE principals(tid TEXT, "
                       "nid TEXT, category TEXT, characters TEXT,"
                       "FOREIGN KEY (tid) REFERENCES basics(tid),"
                       "FOREIGN KEY (nid) REFERENCES names(nid),"
                       "PRIMARY KEY (tid,nid,category,characters))")
    with open(Paths.DB_DATA_REMOTE + 'principals', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        last_valid_id = -1
        while line:
            entries = line.split('\t')
            current_id = tid_to_int(entries[0])
            if (current_id == last_valid_id) or is_valid_tid(current_id):
                last_valid_id = current_id
                entries = entries[0:1] + entries[2:4] + entries[5:]
                db_connect.execute("INSERT OR REPLACE INTO principals VALUES (?,?,?,?)", entries)

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def read_crew():
    print('Reading writers & directors to database.')
    db_connect = sqlite3.connect(Paths.LOCAL_DB)
    db_connect.execute("PRAGMA synchronous = 0")
    db_connect.execute(
        "CREATE TABLE writers(tid TEXT, "
        "nid TEXT,"
        "FOREIGN KEY (tid) REFERENCES basics(tid),"
        "FOREIGN KEY (nid) REFERENCES names(nid),"
        "PRIMARY KEY (tid,nid))")
    db_connect.execute(
        "CREATE TABLE directors(tid TEXT, "
        "nid TEXT,"
        "FOREIGN KEY (tid) REFERENCES basics(tid),"
        "FOREIGN KEY (nid) REFERENCES names(nid),"
        "PRIMARY KEY (tid,nid))")
    with open(Paths.DB_DATA_REMOTE + 'crew', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            if is_valid_tid(tid_to_int(entries[0])):
                for director in entries[1].split(','):
                    db_connect.execute("INSERT INTO directors VALUES (?,?)", (entries[0], director))

                for writer in entries[2].split(','):
                    db_connect.execute("INSERT INTO writers VALUES (?,?)", (entries[0], writer))

            line = file.readline().strip()

    db_connect.execute("CREATE INDEX directors_ix ON directors (nid)")
    db_connect.execute("CREATE INDEX writers_ix ON writers (nid)")
    db_connect.commit()
    db_connect.close()


def read_names():
    print('Reading names to database.')
    db_connect = sqlite3.connect(Paths.LOCAL_DB)
    db_connect.execute("PRAGMA synchronous = 0")
    db_connect.execute("CREATE TABLE names(nid TEXT PRIMARY KEY, name TEXT)")
    with open(Paths.DB_DATA_REMOTE + 'names', 'r') as file:
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

    db_connect.execute("CREATE INDEX names_ix ON names (name)")
    db_connect.commit()
    db_connect.close()


DATASETS_TO_READ_FUNCTIONS = {'basics': read_basics, 'names': read_names, 'akas': read_akas,
                              'crew': read_crew, 'principals': read_principals,
                              'ratings': read_ratings}
