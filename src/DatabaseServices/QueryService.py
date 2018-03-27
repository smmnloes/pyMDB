import sqlite3
import time

from DatabaseServices import Paths


def millis():
    return int(round(time.time() * 1000))


def get_movies_by_criteria(request):
    db_connect = sqlite3.connect('file:' + Paths.LOCAL_DB + '?mode=ro', uri=True)
    c = db_connect.cursor()

    query_select = "SELECT b.*,r.averageRating"
    query_from = "FROM basics b, ratings r"
    query_from_items = []
    query_where = " WHERE r.tid=b.tid AND "

    if request['director']:
        query_where += "n1.name='%s' AND d.nid=n1.nid AND d.tid=b.tid AND " % request['director']
        query_from_items.append(',directors d,names n1')

    if request['writer']:
        query_where += "n2.name='%s' AND w.nid=n2.nid AND w.tid=b.tid AND " % request['writer']
        query_from_items.append(',writers w,names n2')

    if request['year_from']:
        query_where += "b.year >=%d AND " % request['year_from']

    if request['year_to']:
        query_where += "b.year <=%d AND " % request['year_to']

    if request['minRatingIMDB']:
        query_where += "r.averageRating>=%.1f AND " % request['minRatingIMDB']

    if request['genres']:
        for genre in request['genres'].split(','):
            query_where += "b.genres LIKE '%{}%' AND ".format(genre)

    query_where = query_where.strip(' AND ')

    for item in query_from_items:
        query_from += item

    query_from = query_from.strip(',')

    query = query_select + " " + query_from + " " + query_where

    print(query)
    time_before = millis()
    c.execute(query)
    print("Time taken: " + str(millis() - time_before) + "ms")
    results = c.fetchall()
    print("Results: {}".format(len(results)))
    return results
