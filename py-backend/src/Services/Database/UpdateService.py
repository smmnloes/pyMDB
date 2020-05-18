import bisect
import gzip
import os
import shutil
import sqlite3
import urllib.request

from App.AppMain import db, create_app
from Config import ConfigService
from Services.Database.QueryService import normalize

DATASETS = ['basics', 'principals', 'names', 'crew', 'ratings']
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
            app.logger.info('Processing {} data.'.format(dataset))
            download_and_unzip_new_data(dataset)
            app.logger.info('Reading {} to database.'.format(dataset))
            DATASETS_TO_READ_FUNCTIONS.get(dataset)()
            delete_downloaded_remote_data(dataset)
            app.logger.info('Finished processing {} data.\n'.format(dataset))

        analyze()
        app.logger.info("Update complete!")

    except (Exception, BaseException) as e:
        app.logger.error("Error while updating: {}".format(str(e)))
        restore_db_last_version()
        raise e


def get_db_connect():
    db_connect = sqlite3.connect(ConfigService.get_movie_db_path())
    db_connect.execute("PRAGMA synchronous = 0")
    db_connect.execute("PRAGMA default_cache_size = 40000")
    return db_connect


def backup_local_db():
    app.logger.info('Backing up last version.')
    current_db_path = ConfigService.get_movie_db_path()
    last_version_path = ConfigService.get_last_version_path()

    if os.path.isfile(current_db_path):
        os.rename(current_db_path, last_version_path)
    else:
        app.logger.warn('No database found, nothing to back up.')


def restore_db_last_version():
    app.logger.info('Restoring last version.')
    current_db_path = ConfigService.get_movie_db_path()
    last_version_path = ConfigService.get_last_version_path()

    if os.path.isfile(last_version_path):
        os.rename(last_version_path, current_db_path)
        app.logger.info('Last version restored!')
    else:
        app.logger.warn("No previous version found! Cannot restore last version!")


def download_and_unzip_new_data(dataset):
    temp_path = ConfigService.get_temp_path()

    unzipped_path = os.path.join(temp_path, dataset)
    zipped_path = unzipped_path + '_zipped'
    app.logger.info('Downloading {} data.'.format(dataset))
    urllib.request.urlretrieve(ConfigService.get_imdb_url() + DATASETS_TO_FILENAMES.get(dataset),
                               zipped_path)

    app.logger.info('Unzipping {} data'.format(dataset))
    with gzip.open(zipped_path) as zipped_file:
        with open(unzipped_path, 'wb') as unzipped_file:
            shutil.copyfileobj(zipped_file, unzipped_file)

    os.remove(zipped_path)


def delete_downloaded_remote_data(dataset):
    app.logger.info('Deleting local {} file'.format(dataset))
    os.remove(os.path.join(ConfigService.get_temp_path(), dataset))


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


def tid_nid_to_int(tid_nid):
    return int(tid_nid[2:])


def analyze():
    app.logger.info("Analyzing.\n")
    db_connect = sqlite3.connect(ConfigService.get_movie_db_path())
    db_connect.execute('ANALYZE')


def read_basics():
    db_connect = get_db_connect()

    with open(os.path.join(ConfigService.get_temp_path(), 'basics'), 'r') as file:
        file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')

            # only add movies which aren't adult
            if (entries[1] == "movie") & (entries[4] == "0"):
                entries_basics = clean_nulls(entries[0:1] + entries[2:3] + entries[5:6] + entries[7:])
                entries_basics[0] = tid_nid_to_int(entries_basics[0])
                title_normalized = normalize(entries_basics[1])
                db_connect.execute("INSERT INTO basics VALUES (?,?,?,?,?,?)",
                                   entries_basics + [title_normalized])
                VALID_IDS.append(entries_basics[0])

            line = file.readline().strip()

        VALID_IDS.sort()
        db_connect.commit()
        db_connect.close()


def read_ratings():
    db_connect = get_db_connect()

    with open(os.path.join(ConfigService.get_temp_path(), 'ratings'), 'r') as file:
        file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            entries[0] = tid_nid_to_int(entries[0])
            if is_valid_tid(entries[0]):
                db_connect.execute("INSERT INTO ratings VALUES (?,?,?)", entries)

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def read_principals():
    db_connect = get_db_connect()

    with open(os.path.join(ConfigService.get_temp_path(), 'principals'), 'r') as file:
        file.readline()
        line = file.readline().strip()

        last_valid_id = -1
        while line:
            entries = line.split('\t')
            if entries[3] in ['actor', 'actress', 'self']:
                entries[0] = tid_nid_to_int(entries[0])
                current_id = entries[0]
                if (current_id == last_valid_id) or is_valid_tid(current_id):
                    last_valid_id = current_id
                    entries[2] = tid_nid_to_int(entries[2])
                    db_connect.execute("INSERT OR REPLACE INTO principals VALUES (?,?)", (entries[0], entries[2]))

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def read_crew():
    db_connect = get_db_connect()

    with open(os.path.join(ConfigService.get_temp_path(), 'crew'), 'r') as file:
        file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            entries[0] = tid_nid_to_int(entries[0])
            if is_valid_tid(entries[0]):
                if entries[1] != '\\N':
                    for director in entries[1].split(','):
                        director = tid_nid_to_int(director)
                        db_connect.execute("INSERT INTO directors VALUES (?,?)", (entries[0], director))

                if entries[2] != '\\N':
                    for writer in entries[2].split(','):
                        writer = tid_nid_to_int(writer)
                        db_connect.execute("INSERT INTO writers VALUES (?,?)", (entries[0], writer))

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def read_names():
    db_connect = get_db_connect()

    with open(os.path.join(ConfigService.get_temp_path(), 'names'), 'r') as file:
        file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')

            if entries[5] != '\\N':
                known_for = entries[5].split(',')
                known_for = [tid_nid_to_int(x) for x in known_for]

                if one_is_valid_tid(known_for):
                    entries[0] = tid_nid_to_int(entries[0])
                    name_normalized = normalize(entries[1])
                    db_connect.execute("INSERT INTO names VALUES (?,?,?)", entries[0:2] + [name_normalized])

            line = file.readline().strip()

    db_connect.commit()
    db_connect.close()


def clean_nulls(entries):
    return [None if entry == '\\N' else entry for entry in entries]


DATASETS_TO_READ_FUNCTIONS = {'basics': read_basics, 'names': read_names,
                              'crew': read_crew, 'principals': read_principals,
                              'ratings': read_ratings}
