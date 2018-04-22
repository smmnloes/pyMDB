from time import time

from sqlalchemy.orm import aliased
from unidecode import unidecode

from DatabaseServices.DatabaseModel import *

MIN_NUM_VOTES = 1000


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


def normalize(to_normalize):
    return unidecode(to_normalize).lower()


def get_movies_by_criteria(request, get_count=False):
    print('Request: \n' + str(request) + '\n')

    query = db.session.query(Basics).outerjoin(Ratings)
    query = query.add_columns(Ratings.averageRating)

    if request['title']:
        title_normalized = normalize(request['title'])
        query = query.filter(Basics.title_nomalized.like('%{}%'.format(title_normalized)))

    if request['director']:
        director_normalized = normalize(request['director'])
        names_alias = aliased(Names)
        query = query.filter(Basics.tid == Directors.tid, Directors.nid == names_alias.nid,
                             names_alias.name_normalized == director_normalized)

    if request['writer']:
        writer_normalized = normalize(request['writer'])
        names_alias = aliased(Names)
        query = query.filter(Basics.tid == Writers.tid, Writers.nid == names_alias.nid,
                             names_alias.name_normalized == writer_normalized)

    if request['year_from']:
        query = query.filter(Basics.year >= request['year_from'])

    if request['year_to']:
        query = query.filter(Basics.year <= request['year_to'])

    if request['minRatingIMDB']:
        query = query.filter(Ratings.averageRating >= request['minRatingIMDB'], Ratings.tid == Basics.tid,
                             Ratings.numVotes > MIN_NUM_VOTES)

    if request['genres']:
        for genre in request['genres']:
            query = query.filter(Basics.genres.like('%{}%'.format(genre)))

    if request['principals']:
        for principal in request['principals']:
            if principal:
                principal_normalized = normalize(principal)
                names = aliased(Names)
                principals = aliased(Principals)
                query = query.filter(names.name_normalized == principal_normalized, principals.nid == names.nid,
                                     Basics.tid == principals.tid
                                     )

    if get_count:
        return query.count()

    page_size = request['page_size']
    current_page = request['currentPage']
    query = query.order_by(Basics.title_nomalized).limit(page_size).offset((current_page - 1) * page_size)

    # print(query)

    time_before = time()
    results = query.all()
    print("\nQuery time: " + str((time() - time_before) * 1000) + "ms")

    time_before = time()
    results_dict_list = results_to_dict_list(results)
    print("Result processing time: " + str((time() - time_before) * 1000) + "ms")

    print("\nResults: {}".format(len(results)))
    print(results_dict_list)
    print('\n')
    return results_dict_list


def get_number_results(request):
    return get_movies_by_criteria(request, get_count=True)
