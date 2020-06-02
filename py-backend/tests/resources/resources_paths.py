import os

RESOURCES_ROOT = os.path.dirname(os.path.abspath(__file__))
TEST_DB_PATH = os.path.join(RESOURCES_ROOT, 'test_db', 'test.db')
TEST_TEMP_PATH = os.path.join(RESOURCES_ROOT, 'temp')