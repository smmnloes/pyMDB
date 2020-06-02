import os
import unittest
from unittest.mock import patch, MagicMock

from flask import Flask

from model.database_model import *
from resources.resources_paths import TEST_TEMP_PATH, TEST_TEMP_DB_PATH
from services.database import update_service


@patch('services.config.config_service.get_movie_db_path', MagicMock(return_value=TEST_TEMP_DB_PATH))
@patch('services.config.config_service.get_temp_path', MagicMock(return_value=TEST_TEMP_PATH))
class TestUpdateService(unittest.TestCase):
    test_app = None

    @classmethod
    def setUpClass(cls):
        cls.test_app = create_test_app()
        db.init_app(cls.test_app)
        pass

    @classmethod
    def setUp(cls):
        if os.path.exists(TEST_TEMP_DB_PATH):
            os.remove(TEST_TEMP_DB_PATH)
        with cls.test_app.app_context():
            db.create_all()

    def test_read_basics(self):
        update_service.read_basics()
        with self.test_app.app_context():
            self.assertEqual(db.session.query(Basics).count(), 4)
            self.assertEqual(db.session.query(Basics).filter(Basics.primaryTitle == 'Short film').count(), 0)
            self.assertEqual(db.session.query(Basics).filter(Basics.primaryTitle == 'Adult movie').count(), 0)


def create_test_app():
    test_app = Flask(__name__)
    test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_TEMP_DB_PATH
    return test_app
