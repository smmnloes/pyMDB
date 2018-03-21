import sqlite3

from DatabaseServices import Paths


def make_query(request):
    db_connect = sqlite3.connect('file:' + Paths.LOCAL_DB + '?mode=ro', uri=True)
    db_connect.set_trace_callback(print)
    c = db_connect.cursor()
    query = "SELECT b.* from basics b, directors d, writers w, names n1, names n2, ratings r WHERE "

    if request['director']:
        query = query + "n1.name='%s' AND d.nid=n1.nid AND d.tid=b.tid AND " % request['director']
    if request['writer']:
        query = query + "n2.name='%s' AND w.nid=n2.nid AND w.tid=b.tid AND " % request['writer']

    if request['year_from']:
        query = query + "b.year >=%d AND " % request['year_from']

    if request['year_to']:
        query = query + "b.year <=%d AND " % request['year_to']

    if request['minRatingIMDB']:
        query = query + "b.tid=r.tid AND r.averageRating>=%.1f AND " % request['minRatingIMDB']

    for genre in request['genres']:
        query = query + "b.genres LIKE '%{}%' AND ".format(genre)

    query = query.strip(' AND ')

    c.execute(query)
    return c.fetchall()
