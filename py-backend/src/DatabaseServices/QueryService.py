import time

from sqlalchemy.orm import aliased

from App.AppMain import db, create_app
from DatabaseServices.DatabaseModel import *

app = create_app()
app.app_context().push()


def millis():
    return int(round(time.time() * 1000))


def result2dict(result):
    d = {}
    for i in range(0, len(result)):
        d[result._fields[i]] = result[i]
    return d


def get_movies_by_criteria(request):
    query = db.session.query()
    query = query.add_columns(Ratings.averageRating, Basics.primaryTitle, Basics.tid, Basics.runtimeMinutes,
                              Basics.genres, Basics.year)
    query = query.filter(Ratings.tid == Basics.tid)
    names1 = aliased(Names)
    names2 = aliased(Names)
    if request['director']:
        query = query.filter(Basics.tid == Directors.tid, Directors.nid == names1.nid,
                             names1.name == request['director'])

    if request['writer']:
        query = query.filter(Basics.tid == Writers.tid, Writers.nid == names2.nid,
                             names2.name == request['writer'])

    if request['year_from']:
        query = query.filter(Basics.year >= request['year_from'])

    if request['year_to']:
        query = query.filter(Basics.year <= request['year_to'])

    if request['minRatingIMDB']:
        query = query.filter(Ratings.averageRating >= request['minRatingIMDB'])

    if request['genres']:
        for genre in request['genres'].split(','):
            query = query.filter(Basics.genres.like("%{}%".format(genre)))

    print(query)
    time_before = millis()
    results = query.all()
    print("Time taken: " + str(millis() - time_before) + "ms")
    results_dict_list = []
    for r in results:
        results_dict_list.append(result2dict(r))
    print("Results: {}".format(len(results)))
    return results_dict_list
