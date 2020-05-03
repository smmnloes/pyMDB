from time import time

from sqlalchemy import asc, desc
from sqlalchemy.orm import aliased
from unidecode import unidecode

from App.AppMain import create_app
from DatabaseServices.DatabaseModel import *

app = create_app()

MIN_NUM_VOTES = 1000


def results_to_dict_list(results):
    dict_list = []
    for result in results:
        result_tid = result[0].tid
        as_dict = {'tid': result_tid,
                   'primary_title': result[0].primaryTitle,
                   'year': result[0].year,
                   'runtime_minutes': result[0].runtimeMinutes,
                   'genres': None if result[0].genres is None else result[0].genres.split(','),
                   'average_rating': result[1],
                   'principals': get_principals_for_tid(result_tid),
                   'directors': get_directors_for_tid(result_tid),
                   'writers': get_writers_for_tid(result_tid)
                   }
        dict_list.append(as_dict)

    return dict_list


def get_principals_for_tid(tid):
    query = db.session.query().add_columns(Names.name).filter(Principals.tid == tid, Principals.nid == Names.nid)
    return [x[0] for x in query.all()]


def get_directors_for_tid(tid):
    query = db.session.query().add_columns(Names.name).filter(Directors.tid == tid, Names.nid == Directors.nid)
    return [x[0] for x in query.all()]


def get_writers_for_tid(tid):
    query = db.session.query().add_columns(Names.name).filter(Writers.tid == tid, Names.nid == Writers.nid)
    return [x[0] for x in query.all()]


def normalize(to_normalize):
    return unidecode(to_normalize).lower()


def get_movies_by_criteria(request, get_count=False):
    app.logger.debug('Request for movie by criteria: \n' + str(request) + '\n')

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

    if request['min_rating_imdb']:
        query = query.filter(Ratings.averageRating >= request['min_rating_imdb'], Ratings.tid == Basics.tid,
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

    sort_by = request['sort_by']
    if sort_by == 'Title':
        query = query.order_by(asc(Basics.primaryTitle))
    elif sort_by == 'Year':
        query = query.order_by(desc(Basics.year))
    elif sort_by == 'Rating':
        query = query.order_by(desc(Ratings.averageRating))

    results_per_page = int(request['results_per_page'])
    current_page = int(request['current_page'])
    query = query.limit(results_per_page).offset((current_page - 1) * results_per_page)

    time_before = time()
    results = query.all()
    app.logger.debug("\nQuery time: " + str((time() - time_before) * 1000) + "ms")

    time_before = time()
    results_dict_list = results_to_dict_list(results)
    app.logger.debug("Result processing time: " + str((time() - time_before) * 1000) + "ms")

    app.logger.debug("\nResults: {}".format(len(results)))
    app.logger.debug(results_dict_list)
    app.logger.debug('\n')
    return results_dict_list


def get_number_results(request):
    return get_movies_by_criteria(request, get_count=True)


def get_movie_by_tid(request):
    app.logger.debug('Request for movie by tid: \n' + str(request) + '\n')

    query = db.session.query(Basics).outerjoin(Ratings)
    query = query.add_columns(Ratings.averageRating)
    query = query.filter(Basics.tid == request['tid'])

    return results_to_dict_list(query.all())
