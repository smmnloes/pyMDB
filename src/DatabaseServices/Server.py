import sqlite3

from flask import Flask
from flask_restful import Api

from DatabaseServices import Paths

app = Flask(__name__)
api = Api(app)


class Movie:
    def get(self, director, yearFrom, yearTo):
        db_connect = sqlite3.connect(Paths.LOCAL_DB)
        c = db_connect.cursor()
        result = c.execute('SELECT * FROM basics b, crew c, names n WHERE n.name = ? AND n.nid ')