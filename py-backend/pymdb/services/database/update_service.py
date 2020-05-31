import os
import sqlite3

from app import app_main
from constants.constants import DATASET_BASICS, DATASET_AKAS, DATASET_PRINCIPALS, DATASET_NAMES, DATASET_CREW, \
    DATASET_RATINGS, TABLE_FTS
from services.config import config_service
from util.util import tid_nid_to_int, ordered_list_contains_number, clean_nulls, normalize
from . import backup_service, download_service

DATASETS = [DATASET_BASICS, DATASET_AKAS, DATASET_PRINCIPALS, DATASET_NAMES, DATASET_CREW, DATASET_RATINGS]

VALID_IDS = []
LAST_VALID_ID = -1


def update_db():
    backup_service.backup_local_db()

    with app_main.pymdb_app.app_context():
        app_main.db.create_all()

    try:
        for dataset in DATASETS:
            app_main.logger.info('Processing {} data.'.format(dataset))
            download_service.download_and_unzip_datasets(dataset)
            app_main.logger.info('Reading {} to database.'.format(dataset))
            DATASETS_TO_READ_FUNCTIONS.get(dataset)()
            download_service.delete_downloaded_dataset(dataset)
            app_main.logger.info('Finished processing {} data.\n'.format(dataset))

        analyze()
        app_main.logger.info("Update complete!")

    except (Exception, BaseException) as e:
        app_main.logger.error("Error while updating: {}".format(str(e)))
        backup_service.restore_db_last_version()
        raise e


def get_db_connect():
    db_connect = sqlite3.connect(config_service.get_movie_db_path())
    db_connect.execute("PRAGMA synchronous = 0")
    db_connect.execute("PRAGMA default_cache_size = 40000")
    return db_connect


def is_valid_tid(tid):
    return ordered_list_contains_number(tid, VALID_IDS)


def one_is_valid_tid(to_check):
    for x in to_check:
        if is_valid_tid(x):
            return True
    return False


def analyze():
    app_main.logger.info("Analyzing.\n")
    db_connect = get_db_connect()
    db_connect.execute('ANALYZE')
    db_connect.close()


def read_to_db(dataset_name, entries_to_row_func, pre_op=None, post_op=None):
    db_connect = get_db_connect()
    if pre_op:
        pre_op(db_connect=db_connect)

    with open(os.path.join(config_service.get_temp_path(), dataset_name), 'r') as file:
        file.readline()
        line = file.readline().strip()

        while line:
            entries = line.split('\t')
            entries = clean_nulls(entries)
            entries_to_row_func(entries, db_connect)
            line = file.readline().strip()

    if post_op:
        post_op()
    db_connect.commit()
    db_connect.close()


def read_basics():
    def entries_to_row(entries, db_connect):
        if (entries[1] == "movie") & (entries[4] == "0"):
            entries_basics = entries[0:1] + entries[2:3] + entries[5:6] + entries[7:]
            entries_basics[0] = tid_nid_to_int(entries_basics[0])
            db_connect.execute("INSERT INTO basics VALUES (?,?,?,?,?)",
                               entries_basics)
            VALID_IDS.append(entries_basics[0])

    read_to_db(dataset_name=DATASET_BASICS, entries_to_row_func=entries_to_row, post_op=VALID_IDS.sort)


def read_ratings():
    def entries_to_row(entries, db_connect):
        entries[0] = tid_nid_to_int(entries[0])
        if is_valid_tid(entries[0]):
            db_connect.execute("INSERT INTO ratings VALUES (?,?,?)", entries)

    read_to_db(dataset_name=DATASET_RATINGS, entries_to_row_func=entries_to_row)


def read_principals():
    def entries_to_row(entries, db_connect):
        if entries[3] in ['actor', 'actress', 'self']:
            entries[0] = tid_nid_to_int(entries[0])
            current_id = entries[0]
            global LAST_VALID_ID
            if (current_id == LAST_VALID_ID) or is_valid_tid(current_id):
                LAST_VALID_ID = current_id
                entries[2] = tid_nid_to_int(entries[2])
                db_connect.execute("INSERT OR REPLACE INTO principals VALUES (?,?)", (entries[0], entries[2]))

    read_to_db(dataset_name=DATASET_PRINCIPALS, entries_to_row_func=entries_to_row)


def read_crew():
    def entries_to_row(entries, db_connect):
        entries[0] = tid_nid_to_int(entries[0])
        if is_valid_tid(entries[0]):
            if entries[1]:
                for director in entries[1].split(','):
                    director = tid_nid_to_int(director)
                    db_connect.execute("INSERT INTO directors VALUES (?,?)", (entries[0], director))

            if entries[2]:
                for writer in entries[2].split(','):
                    writer = tid_nid_to_int(writer)
                    db_connect.execute("INSERT INTO writers VALUES (?,?)", (entries[0], writer))

    read_to_db(dataset_name=DATASET_CREW, entries_to_row_func=entries_to_row)


def read_names():
    def entries_to_row(entries, db_connect):
        if entries[5]:
            known_for = entries[5].split(',')
            known_for = [tid_nid_to_int(x) for x in known_for]

            if one_is_valid_tid(known_for):
                entries[0] = tid_nid_to_int(entries[0])
                name_normalized = normalize(entries[1])
                db_connect.execute("INSERT INTO names VALUES (?,?,?)", entries[0:2] + [name_normalized])

    read_to_db(dataset_name=DATASET_NAMES, entries_to_row_func=entries_to_row)


def read_akas():
    def pre(db_connect):
        db_connect.execute("CREATE VIRTUAL TABLE {} USING fts5(tid, title)".format(TABLE_FTS))

    def entries_to_row(entries, db_connect):
        entries[0] = tid_nid_to_int(entries[0])
        if is_valid_tid(entries[0]):
            entries[2] = normalize(entries[2])
            db_connect.execute("INSERT INTO {} VALUES (?,?)".format(TABLE_FTS), (entries[0], entries[2]))

    read_to_db(dataset_name=DATASET_AKAS, entries_to_row_func=entries_to_row, pre_op=pre)


DATASETS_TO_READ_FUNCTIONS = {DATASET_BASICS: read_basics, DATASET_NAMES: read_names,
                              DATASET_CREW: read_crew, DATASET_PRINCIPALS: read_principals,
                              DATASET_RATINGS: read_ratings, DATASET_AKAS: read_akas}
