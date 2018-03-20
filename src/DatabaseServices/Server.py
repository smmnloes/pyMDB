import sqlite3

from flask import Flask, jsonify
from flask_restful import Api, Resource

from DatabaseServices import Paths

app = Flask(__name__)
api = Api(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def process_string(string):
    return '%' + string + '%'


class Movie(Resource):
    def get(self, director, year_from, year_to, min_rating, genre_1, genre_2):
        genre_1 = process_string(genre_1)
        genre_2 = process_string(genre_2)

        db_connect = sqlite3.connect(Paths.LOCAL_DB)
        db_connect.row_factory = dict_factory
        c = db_connect.cursor()

        query = c.execute('SELECT b.tid, b.primaryTitle, b.year, b.runtimeMinutes, b.genres, r.averageRating '
                          'FROM basics b, directors d, names n, ratings r '
                          'WHERE n.name = ? '
                          'AND n.nid = d.director '
                          'AND d.tid = b.tid '
                          'AND b.year BETWEEN ? AND ? '
                          'AND r.tid = b.tid '
                          'AND r.averageRating >= ? '
                          'AND b.genres LIKE ? '
                          'AND b.genres LIKE ?',
                          (director, year_from, year_to, min_rating, genre_1, genre_2))
        return jsonify(query.fetchall())


api.add_resource(Movie, '/query/<director>/<year_from>/<year_to>/<min_rating>/<genre_1>/<genre_2>')

app.run(port=5002)
