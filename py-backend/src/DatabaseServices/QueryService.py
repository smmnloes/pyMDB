import time

from sqlalchemy.orm import aliased

from DatabaseServices.DatabaseModel import *


def millis():
    return int(round(time.time() * 1000))


def result2dict(result):
    d = {}
    for i in range(0, len(result)):
        d[result._fields[i]] = result[i]
    return d


def get_movies_by_criteria(request):
    query = db.session.query()
    query = query.add_columns(Basics.primaryTitle, Basics.tid, Basics.runtimeMinutes,
                              Basics.year)

    if request['director']:
        names_alias = aliased(Names)
        query = query.filter(Basics.tid == Directors.tid, Directors.nid == names_alias.nid,
                             names_alias.name == request['director'])

    if request['writer']:
        names_alias = aliased(Names)
        query = query.filter(Basics.tid == Writers.tid, Writers.nid == names_alias.nid,
                             names_alias.name == request['writer'])

    if request['year_from']:
        query = query.filter(Basics.year >= request['year_from'])

    if request['year_to']:
        query = query.filter(Basics.year <= request['year_to'])

    if request['minRatingIMDB']:
        query = query.filter(Ratings.averageRating >= request['minRatingIMDB'], Ratings.tid == Basics.tid)

    if request['genres']:
        for genre in request['genres'].split(','):
            genres_alias = aliased(Genres)
            query = query.filter(genres_alias.tid == Basics.tid, genres_alias.genre == genre)

    print(query)
    time_before = millis()
    results = query.all()
    print("Time taken: " + str(millis() - time_before) + "ms")
    results_dict_list = []
    for r in results:
        results_dict_list.append(result2dict(r))
    print("Results: {}".format(len(results)))
    return results_dict_list
