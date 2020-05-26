from time import time

from sqlalchemy import asc, desc, text
from sqlalchemy.orm import aliased
from unidecode import unidecode

from App.AppMain import create_app
from Model.DatabaseModel import *

app = create_app()

MIN_NUM_VOTES = 1000
LIMIT_FTS_SEARCH_RESULTS = 5000


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

    title_criteria = request['title']
    if title_criteria:
        title_normalized = normalize(title_criteria)
        tids_fts = get_tids_fts(get_count, request, title_normalized)
        query = query.filter(Basics.tid.in_(tids_fts))

    director_criteria = request['director']
    if director_criteria:
        director_normalized = normalize(director_criteria)
        names_alias = aliased(Names)
        query = query.filter(Basics.tid == Directors.tid, Directors.nid == names_alias.nid,
                             names_alias.name_normalized == director_normalized)

    writer_criteria = request['writer']
    if writer_criteria:
        writer_normalized = normalize(writer_criteria)
        names_alias = aliased(Names)
        query = query.filter(Basics.tid == Writers.tid, Writers.nid == names_alias.nid,
                             names_alias.name_normalized == writer_normalized)

    year_from_criteria = request['year_from']
    if year_from_criteria:
        query = query.filter(Basics.year >= year_from_criteria)

    year_to_criteria = request['year_to']
    if year_to_criteria:
        query = query.filter(Basics.year <= year_to_criteria)

    min_rating_imdb_criteria = request['min_rating_imdb']
    if min_rating_imdb_criteria:
        query = query.filter(Ratings.averageRating >= min_rating_imdb_criteria,
                             Ratings.numVotes > MIN_NUM_VOTES)

    genres_criteria = request['genres']
    if genres_criteria:
        for genre in genres_criteria:
            query = query.filter(Basics.genres.like('%{}%'.format(genre)))

    principals_criteria = request['principals']
    if principals_criteria:
        for principal in principals_criteria:
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
    elif sort_by == 'Relevance':
        # do nothing here as the results are already sorted by fts5-rank (see above)
        pass

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
    app.logger.debug('\n\n\n')
    return results_dict_list


def get_tids_fts(get_count, request, title_normalized):
    order_by_clause = "ORDER BY RANK" if (request['sort_by'] == 'Relevance' and not get_count) else ""
    query_text = text(
        "SELECT DISTINCT tid FROM {} WHERE title MATCH :keyword {} LIMIT :limit".format(TABLE_FTS, order_by_clause))
    query_text = query_text.bindparams(keyword=title_normalized, limit=LIMIT_FTS_SEARCH_RESULTS)
    result = db.session.execute(query_text).fetchall()
    tid_list = [row['tid'] for row in result]
    return tid_list


def get_movie_by_tid(request):
    app.logger.debug('Request for movie by tid: \n' + str(request) + '\n')

    query = db.session.query(Basics).outerjoin(Ratings)
    query = query.add_columns(Ratings.averageRating)
    query = query.filter(Basics.tid == request['tid'])

    return results_to_dict_list(query.all())
