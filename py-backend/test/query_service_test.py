import unittest
from unittest.mock import patch, MagicMock

from model.database_model import *
from resources.resources_paths import TEST_QUERY_DB_PATH
from services.database import query_service
from test_queries import *
from test_utils import create_test_app


@patch('app.app_main.logger', MagicMock())
@patch('services.config.config_service.get_movie_db_path', MagicMock(return_value=TEST_QUERY_DB_PATH))
class TestQueryService(unittest.TestCase):
    test_app = None

    @classmethod
    def setUpClass(cls):
        cls.test_app = create_test_app(TEST_QUERY_DB_PATH)
        db.init_app(cls.test_app)
        pass

    def test_empty_query(self):
        with self.test_app.app_context():
            query4 = QueryBuilder().query
            self.assertEqual(len(query_service.get_movies_by_criteria(query4)), 6)

    def test_query_title(self):
        with self.test_app.app_context():
            query1 = QueryBuilder().with_title("Die Hard").query
            self.assertEqual(query_service.get_movies_by_criteria(query1), [die_hard_result])

            query2 = QueryBuilder().with_title("Vom Winde verweht").query
            self.assertEqual(query_service.get_movies_by_criteria(query2), [gone_with_the_wind_result])

            query3 = QueryBuilder().with_title("Once upon Hollywood").query
            self.assertEqual(query_service.get_movies_by_criteria(query3), [once_upon_a_time_result])

    def test_query_genres(self):
        with self.test_app.app_context():
            query1 = QueryBuilder().with_genre("Romance").query
            self.assertEqual(query_service.get_movies_by_criteria(query1), [gone_with_the_wind_result])

            query2 = QueryBuilder().with_genre("Comedy").with_genre("Drama").query
            self.assertEqual(query_service.get_movies_by_criteria(query2), [once_upon_a_time_result])

            query3 = QueryBuilder().with_genre("Romance").with_genre("Crime").query
            self.assertEqual(query_service.get_movies_by_criteria(query3), [])

            query4 = QueryBuilder().with_genre("Action").query
            self.assertEqual(query_service.get_movies_by_criteria(query4), [die_hard_result, inception_result])

    def test_query_min_rating(self):
        with self.test_app.app_context():
            query1 = QueryBuilder().with_min_rating(9.5).query
            self.assertEqual(query_service.get_movies_by_criteria(query1), [once_upon_a_time_result])

            query2 = QueryBuilder().with_min_rating(8.0).query
            self.assertEqual(query_service.get_movies_by_criteria(query2),
                             [gone_with_the_wind_result, once_upon_a_time_result])

            query3 = QueryBuilder().with_min_rating(3.0).query
            self.assertEqual(query_service.get_movies_by_criteria(query3),
                             [gone_with_the_wind_result, twelve_angry_result, once_upon_a_time_result])

    def test_query_director(self):
        with self.test_app.app_context():
            query1 = QueryBuilder().with_director("Victor Fleming").query
            self.assertEqual(query_service.get_movies_by_criteria(query1), [gone_with_the_wind_result])

            query2 = QueryBuilder().with_director("George Cukor").query
            self.assertEqual(query_service.get_movies_by_criteria(query2), [gone_with_the_wind_result])

            query3 = QueryBuilder().with_director("Unknown director").query
            self.assertEqual(query_service.get_movies_by_criteria(query3), [])

            query4 = QueryBuilder().with_director("Quentin Tarantino").query
            self.assertEqual(query_service.get_movies_by_criteria(query4), [once_upon_a_time_result])

    def test_query_writer(self):
        with self.test_app.app_context():
            query1 = QueryBuilder().with_writer("Christopher Nolan").query
            self.assertEqual(query_service.get_movies_by_criteria(query1), [inception_result])

            query2 = QueryBuilder().with_writer("Unknown director").query
            self.assertEqual(query_service.get_movies_by_criteria(query2), [])

            query3 = QueryBuilder().with_writer("Margaret Mitchell").query
            self.assertEqual(query_service.get_movies_by_criteria(query3), [gone_with_the_wind_result])

            query4 = QueryBuilder().with_writer("Sidney Howard").query
            self.assertEqual(query_service.get_movies_by_criteria(query4), [gone_with_the_wind_result])

    def test_query_year_from_to(self):
        with self.test_app.app_context():
            query1 = QueryBuilder().with_year_from(2018).query
            self.assertEqual(query_service.get_movies_by_criteria(query1), [once_upon_a_time_result])

            query2 = QueryBuilder().with_year_from(1939).query
            self.assertEqual(len(query_service.get_movies_by_criteria(query2)), 5)

            query3 = QueryBuilder().with_year_to(1939).query
            self.assertEqual(query_service.get_movies_by_criteria(query3), [gone_with_the_wind_result])

            query4 = QueryBuilder().with_year_to(2019).query
            self.assertEqual(len(query_service.get_movies_by_criteria(query4)), 5)

            query5 = QueryBuilder().with_year_to(2019).with_year_from(2010).query
            self.assertEqual(query_service.get_movies_by_criteria(query5), [inception_result, once_upon_a_time_result])

    def test_query_principals(self):
        with self.test_app.app_context():
            query1 = QueryBuilder().with_principal("Clark Gable").query
            self.assertEqual(query_service.get_movies_by_criteria(query1), [gone_with_the_wind_result])

            query2 = QueryBuilder().with_principal("Clark Gable").with_principal("Vivien Leigh").with_principal(
                "Thomas Mitchell").query
            self.assertEqual(query_service.get_movies_by_criteria(query2), [gone_with_the_wind_result])

            query3 = QueryBuilder().with_principal("Leonardo DiCaprio").query
            self.assertEqual(query_service.get_movies_by_criteria(query3), [inception_result, once_upon_a_time_result])

            query4 = QueryBuilder().with_principal("Unkown principal").query
            self.assertEqual(query_service.get_movies_by_criteria(query4), [])

    def test_query_sorting(self):
        with self.test_app.app_context():
            query1 = QueryBuilder().with_title("upon").sort_by_relevance().query
            self.assertEqual(query_service.get_movies_by_criteria(query1), [once_upon_a_time_result, fake_movie_result])

            query2 = QueryBuilder().sort_by_rating().query
            self.assertEqual(query_service.get_movies_by_criteria(query2),
                             [once_upon_a_time_result, gone_with_the_wind_result, twelve_angry_result, die_hard_result,
                              inception_result, fake_movie_result])

            query3 = QueryBuilder().sort_by_title().query
            self.assertEqual(query_service.get_movies_by_criteria(query3),
                             [twelve_angry_result, die_hard_result, gone_with_the_wind_result, inception_result,
                              once_upon_a_time_result, fake_movie_result])

            query4 = QueryBuilder().sort_by_year().query
            self.assertEqual(query_service.get_movies_by_criteria(query4),
                             [once_upon_a_time_result, inception_result, die_hard_result, twelve_angry_result,
                              gone_with_the_wind_result, fake_movie_result])

    def test_number_results(self):
        with self.test_app.app_context():
            query1 = QueryBuilder().with_results_per_page(5).query
            self.assertEqual(len(query_service.get_movies_by_criteria(query1)), 5)

            query2 = QueryBuilder().with_results_per_page(10).query
            self.assertEqual(len(query_service.get_movies_by_criteria(query2)), 6)