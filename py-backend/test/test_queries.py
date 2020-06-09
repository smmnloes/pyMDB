title_only = {
    "director": "",
    "writer": "",
    "genres": None,
    "min_rating_imdb": None,
    "year_from": None,
    "year_to": None,
    "principals": [
        "",
        "",
        ""
    ],
    "title": "Die Hard",
    "results_per_page": "15",
    "current_page": "1",
    "sort_by": "Relevance"
}

die_hard_result = {'tid': 3,
                   'primary_title':
                       'Die Hard',
                   'year': 1988,
                   'runtime_minutes': 132,
                   'genres': ['Action', 'Thriller'],
                   'average_rating': 2.5,
                   'principals': ['Bruce Willis'],
                   'directors': ['John McTiernan'],
                   'writers': ['Roderick Thorp']}

gone_with_the_wind_result = {'average_rating': 8.1,
                             'directors': ['Victor Fleming', 'George Cukor'],
                             'genres': ['Romance', 'Drama'],
                             'primary_title': 'Gone with the wind',
                             'principals': ['Clark Gable', 'Vivien Leigh', 'Thomas Mitchell'],
                             'runtime_minutes': 220,
                             'tid': 1,
                             'writers': ['Margaret Mitchell', 'Sidney Howard'],
                             'year': 1939}

once_upon_a_time_result = {'average_rating': 9.9,
                           'directors': ['Quentin Tarantino'],
                           'genres': ['Comedy', 'Drama'],
                           'primary_title': 'Once upon a Time in Hollywood',
                           'principals': ['Leonardo DiCaprio'],
                           'runtime_minutes': 161,
                           'tid': 5,
                           'writers': ['Quentin Tarantino'],
                           'year': 2019}

inception_result = {'average_rating': None,
                    'directors': ['Christopher Nolan'],
                    'genres': ['Action', 'Adventure', 'Sci-Fi'],
                    'primary_title': 'Inception',
                    'principals': ['Leonardo DiCaprio'],
                    'runtime_minutes': 148,
                    'tid': 4,
                    'writers': ['Christopher Nolan'],
                    'year': 2010}

twelve_angry_result = {'average_rating': 7.6,
                       'directors': ['Sidney Lumet'],
                       'genres': ['Crime', ' Drama'],
                       'primary_title': '12 Angry Men',
                       'principals': ['Henry Fonda'],
                       'runtime_minutes': 120,
                       'tid': 2,
                       'writers': ['Reginald Rose'],
                       'year': 1950}

fake_movie_result = {'average_rating': None,
                     'directors': [],
                     'genres': ['Fake'],
                     'primary_title': 'Upon these fake movies',
                     'principals': [],
                     'runtime_minutes': 120,
                     'tid': 6,
                     'writers': [],
                     'year': None}


class QueryBuilder:
    def __init__(self):
        self.query = {
            "director": "",
            "writer": "",
            "genres": [],
            "min_rating_imdb": None,
            "year_from": None,
            "year_to": None,
            "principals": [],
            "title": "",
            "results_per_page": "15",
            "current_page": "1",
            "sort_by": "Relevance"
        }

    def with_director(self, director):
        self.query["director"] = director
        return self

    def with_title(self, title):
        self.query["title"] = title
        return self

    def with_genre(self, genre):
        self.query["genres"] = self.query["genres"] + [genre]
        return self

    def with_min_rating(self, min_rating):
        self.query["min_rating_imdb"] = min_rating
        return self

    def with_writer(self, writer):
        self.query["writer"] = writer
        return self

    def with_year_from(self, year_from):
        self.query["year_from"] = year_from
        return self

    def with_year_to(self, year_to):
        self.query["year_to"] = year_to
        return self

    def with_principal(self, principal):
        self.query["principals"] = self.query["principals"] + [principal]
        return self

    def sort_by_relevance(self):
        self.query["sort_by"] = "Relevance"
        return self

    def sort_by_year(self):
        self.query["sort_by"] = "Year"
        return self

    def sort_by_rating(self):
        self.query["sort_by"] = "Rating"
        return self

    def sort_by_title(self):
        self.query["sort_by"] = "Title"
        return self

    def with_results_per_page(self, results):
        self.query["results_per_page"] = results
        return self
