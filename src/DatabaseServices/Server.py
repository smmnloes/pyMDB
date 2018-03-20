import sqlite3

from flask import Flask
from flask_restful import Api

from DatabaseServices import Paths

app = Flask(__name__)
api = Api(app)


class Movie:
    def get(self, director, year_from, year_to):
        db_connect = sqlite3.connect(Paths.LOCAL_DB)
        c = db_connect.cursor()
        result = c.execute('SELECT b.primaryTitle FROM basics b, directors d, names n WHERE n.name = ? '
                           'AND n.nid = d.director AND d.tid = b.tid AND '
                           'b.year BETWEEN ? AND ?', (director, year_from, year_to))
        return result
