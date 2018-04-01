import time

from sqlalchemy.orm import aliased

from App.AppMain import create_app
from DatabaseServices.DatabaseModel import *

app = create_app()
app.app_context().push()


def millis():
    return int(round(time.time() * 1000))


def results_to_dict_list(results):
    dict_list = []
    last_tid = -1
    as_dict = None
    for result in results:
        if result[0] != last_tid:
            last_tid = result[0]
            if as_dict is not None:
                dict_list.append(as_dict)
            as_dict = {'tid': result[0].tid,
                       'primaryTitle': result[0].primaryTitle,
                       'year': result[0].year,
                       'runtimeMinutes': result[0].runtimeMinutes,
                       'averageRating': result[1],
                       'genres': [result[2]]
                       }
        else:
            as_dict['genres'].append(result[2])

    return dict_list


def get_movies_by_criteria(request):
    query = db.session.query(Basics).outerjoin(Ratings, Genres)
    query = query.add_columns(Ratings.averageRating, Genres.genre)

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

    results_dict_list = results_to_dict_list(results)
    print("Results: {}".format(len(results)))
    return results_dict_list
