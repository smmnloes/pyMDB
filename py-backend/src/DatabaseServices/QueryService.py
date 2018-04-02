from time import time

from sqlalchemy.orm import aliased

from App.AppMain import create_app
from DatabaseServices.DatabaseModel import *

app = create_app()
app.app_context().push()


def results_to_dict_list(results):
    dict_list = []
    for result in results:
        as_dict = {'tid': result[0].tid,
                   'primaryTitle': result[0].primaryTitle,
                   'year': result[0].year,
                   'runtimeMinutes': result[0].runtimeMinutes,
                   'genres': None if result[0].genres is None else result[0].genres.split(','),
                   'averageRating': result[1],
                   'principals': get_principals_for_tid(result[0].tid),
                   'directors': get_directors_for_tid(result[0].tid)
                   }
        dict_list.append(as_dict)

    return dict_list


def get_principals_for_tid(tid):
    query = db.session.query().add_columns(Names.name).filter(Principals.tid == tid, Principals.nid == Names.nid)
    return [x[0] for x in query.all()]


def get_directors_for_tid(tid):
    query = db.session.query().add_columns(Names.name).filter(Directors.tid == tid, Names.nid == Directors.nid)
    return [x[0] for x in query.all()]


def get_movies_by_criteria(request):
    print('Request: \n' + str(request) + '\n')
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
        for genre in request['genres']:
            query = query.filter(Basics.genres.like('%{}%'.format(genre)))

    if request['principals']:
        for principal in request['principals']:
            names = aliased(Names)
            principals = aliased(Principals)
            query = query.filter(Basics.tid == principals.tid, principals.nid == names.nid, names.name == principal)

    print(query)

    time_before = time()
    results = query.all()
    print("\nQuery time: " + str((time() - time_before) * 1000) + "ms")

    time_before = time()
    results_dict_list = results_to_dict_list(results)
    print("Result processing time: " + str((time() - time_before) * 1000) + "ms")

    print("\nResults: {}".format(len(results)))
    print(results_dict_list)
    print('\n\n\n')
    return results_dict_list
