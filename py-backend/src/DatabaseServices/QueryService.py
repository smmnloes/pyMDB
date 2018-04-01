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

    for result in results:
        as_dict = {'tid': result[0].tid,
                   'primaryTitle': result[0].primaryTitle,
                   'year': result[0].year,
                   'runtimeMinutes': result[0].runtimeMinutes,
                   'genres': result[0].genres.split(','),
                   'averageRating': result[1]
                   }
        dict_list.append(as_dict)

    return dict_list


def get_movies_by_criteria(request):
    query = db.session.query(Basics).outerjoin(Ratings)
    query = query.add_columns(Ratings.averageRating)

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
            query = query.filter(Basics.genres.like('%{}%'.format(genre)))

    print(query)
    time_before = millis()
    results = query.all()
    print("Time taken: " + str(millis() - time_before) + "ms")

    results_dict_list = results_to_dict_list(results)
    print("Results: {}".format(len(results)))
    return results_dict_list
