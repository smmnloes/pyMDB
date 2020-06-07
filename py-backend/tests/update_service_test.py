import os
import unittest
from unittest.mock import patch, MagicMock

from flask import Flask
from sqlalchemy import text

from constants.constants import TABLE_FTS
from model.database_model import *
from resources.resources_paths import TEST_TEMP_PATH, TEST_TEMP_DB_PATH
from services.database import update_service
from util.util import normalize


def is_valid_tid_mock(tid):
    valid_ids = [1, 10]
    return True if tid in valid_ids else False


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

    @patch('services.database.update_service.is_valid_tid', MagicMock(return_value=True))
    def test_read_basics(self):
        update_service.read_basics()
        with self.test_app.app_context():
            self.assertEqual(db.session.query(Basics).count(), 4)
            self.assertEqual(db.session.query(Basics).filter(Basics.primaryTitle == 'primaryTitle').count(), 0)
            self.assertEqual(db.session.query(Basics).filter(Basics.primaryTitle == 'Short film').count(), 0)
            self.assertEqual(db.session.query(Basics).filter(Basics.primaryTitle == 'Adult movie').count(), 0)

    @patch('services.database.update_service.is_valid_tid', MagicMock(return_value=True))
    def test_read_ratings(self):
        update_service.read_ratings()
        with self.test_app.app_context():
            self.assertEqual(db.session.query(Ratings).count(), 3)
            self.assertEqual(db.session.query(Ratings).filter(Ratings.averageRating >= 6.0).count(), 2)
            self.assertEqual(db.session.query(Ratings).filter(Ratings.numVotes == 1301).count(), 1)

    @patch('services.database.update_service.is_valid_tid', MagicMock(return_value=True))
    def test_read_principals(self):
        update_service.read_principals()
        with self.test_app.app_context():
            self.assertEqual(db.session.query(Principals).count(), 5)
            self.assertEqual(db.session.query(Principals).filter(Principals.tid == 'tconst').count(), 0)
            self.assertEqual(
                db.session.query(Principals).filter(Principals.tid == 2, Principals.nid == 721526).count(), 0)

    @patch('services.database.update_service.is_valid_tid', MagicMock(return_value=True))
    def test_read_crew(self):
        update_service.read_crew()
        with self.test_app.app_context():
            self.assertEqual(db.session.query(Directors).count(), 5)
            self.assertEqual(db.session.query(Directors).filter(Directors.tid == 'tconst').count(), 0)
            self.assertEqual(db.session.query(Directors).filter(Directors.tid == 1).count(), 1)
            self.assertEqual(db.session.query(Directors).filter(Directors.tid == 2).count(), 2)
            self.assertEqual(db.session.query(Directors).filter(Directors.tid == 2, Directors.nid == 2).count(), 1)
            self.assertEqual(db.session.query(Directors).filter(Directors.nid == 1).count(), 3)

            self.assertEqual(db.session.query(Writers).count(), 3)
            self.assertEqual(db.session.query(Writers).filter(Writers.tid == 'tconst').count(), 0)
            self.assertEqual(db.session.query(Writers).filter(Writers.tid == 4).count(), 2)
            self.assertEqual(db.session.query(Writers).filter(Writers.nid == 4).count(), 2)
            self.assertEqual(db.session.query(Writers).filter(Writers.nid == 4, Writers.tid == 3).count(), 1)

    @patch('services.database.update_service.is_valid_tid', MagicMock(return_value=True))
    def test_read_names(self):
        update_service.read_names()
        with self.test_app.app_context():
            self.assertEqual(db.session.query(Names).count(), 3)
            self.assertEqual(db.session.query(Names).filter(Names.name == "Fred Astaire").count(), 1)
            self.assertEqual(db.session.query(Names).filter(Names.name == "Lauren Bacall").count(), 1)
            self.assertEqual(db.session.query(Names).filter(Names.name == "Brigitte Bardot").count(), 1)

    @patch('services.database.update_service.is_valid_tid', MagicMock(return_value=True))
    def test_read_akas(self):
        update_service.read_akas()
        with self.test_app.app_context():
            self.assertEqual(len(get_fts_results("Karmensita")), 1)
            self.assertEqual(len(get_fts_results("Карменсіта")), 1)
            self.assertEqual(len(get_fts_results("Le clown et ses chiens")), 1)
            self.assertEqual(len(get_fts_results("Le clown")), 1)
            self.assertEqual(len(get_fts_results("clown chiens")), 1)
            self.assertEqual(len(get_fts_results("哀れなピエロ")), 1)
            self.assertEqual(len(get_fts_results("szegény pierrot")), 1)
            self.assertEqual(len(get_fts_results("pierrot")), 1)

    @patch('services.database.update_service.is_valid_tid', new=is_valid_tid_mock)
    def test_valid_tids(self):
        update_service.read_names()
        with self.test_app.app_context():
            self.assertEqual(db.session.query(Names).count(), 2)
            self.assertEqual(db.session.query(Names).filter(Names.name == "Lauren Bacall").count(), 0)
            self.assertEqual(db.session.query(Names).filter(Names.name == "Brigitte Bardot").count(), 1)
            self.assertEqual(db.session.query(Names).filter(Names.name == "Fred Astaire").count(), 1)


def get_fts_results(keyword):
    title_normalized = normalize(keyword)
    query_text = text(
        'SELECT DISTINCT tid FROM {} WHERE title MATCH :keyword'.format(TABLE_FTS))
    query_text = query_text.bindparams(keyword=title_normalized)
    return db.session.execute(query_text).fetchall()


def create_test_app():
    test_app = Flask(__name__)
    test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_TEMP_DB_PATH
    return test_app
