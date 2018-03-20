import json
import sqlite3

from flask import Flask, jsonify, request
from flask_restful import Api

from DatabaseServices import Paths

app = Flask(__name__)
api = Api(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/query', methods=['POST'])
def query():
    post_query = json.loads(request.data)
    print(post_query)
    db_connect = sqlite3.connect(Paths.LOCAL_DB)
    db_connect.row_factory = dict_factory
    c = db_connect.cursor()

    q = c.execute('SELECT b.tid, b.primaryTitle, b.year, b.runtimeMinutes, b.genres, r.averageRating '
                  'FROM basics b, directors d, names n, ratings r '
                  'WHERE n.name = ? '
                  'AND n.nid = d.director '
                  'AND d.tid = b.tid '
                  'AND b.year BETWEEN ? AND ? '
                  'AND r.tid = b.tid '
                  'AND r.averageRating >= ? '
                  'AND b.genres LIKE ? '
                  'AND b.genres LIKE ?',
                  ('', '', '', '', '', ''))
    return jsonify(q.fetchall())


def start_app():
    app.run(port=5002)
