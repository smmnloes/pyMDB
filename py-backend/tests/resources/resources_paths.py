import os

RESOURCES_ROOT = os.path.dirname(os.path.abspath(__file__))
TEST_DBS_PATH = os.path.join(RESOURCES_ROOT, 'test_dbs')
TEST_TEMP_DB_PATH = os.path.join(TEST_DBS_PATH, 'temp.db')
TEST_QUERY_DB_PATH = os.path.join(TEST_DBS_PATH, 'query.db')
TEST_TEMP_PATH = os.path.join(RESOURCES_ROOT, 'temp')
