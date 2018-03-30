import time

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import aliased

db = None
basics = None
names = None
ratings = None
writers = None
directors = None


def init_query_service():
    db.metadata.reflect(db.engine)
    base = automap_base(metadata=db.metadata)
    base.prepare()
    base.query = db.session.query_property()

    global basics, names, ratings, writers, directors
    basics = base.classes.basics
    names = base.classes.names
    ratings = base.classes.ratings
    writers = base.classes.writers
    directors = base.classes.directors


def millis():
    return int(round(time.time() * 1000))


def result2dict(result):
    d = {}
    for i in range(0, len(result)):
        d[result._fields[i]] = result[i]
    return d


def get_movies_by_criteria(request):
    query = db.session.query()
    query = query.add_columns(ratings.averageRating, basics.primaryTitle, basics.tid, basics.runtimeMinutes,
                              basics.genres, basics.year)
    query = query.filter(ratings.tid == basics.tid)
    names1 = aliased(names)
    names2 = aliased(names)
    if request['director']:
        query = query.filter(basics.tid == directors.tid, directors.nid == names1.nid,
                             names1.name == request['director'])

    if request['writer']:
        query = query.filter(basics.tid == writers.tid, writers.nid == names2.nid,
                             names2.name == request['writer'])

    if request['year_from']:
        query = query.filter(basics.year >= request['year_from'])

    if request['year_to']:
        query = query.filter(basics.year <= request['year_to'])

    if request['minRatingIMDB']:
        query = query.filter(ratings.averageRating >= request['minRatingIMDB'])

    if request['genres']:
        for genre in request['genres'].split(','):
            query = query.filter(basics.genres.like("%{}%".format(genre)))

    print(query)
    time_before = millis()
    results = query.all()
    print("Time taken: " + str(millis() - time_before) + "ms")
    results_dict_list = []
    for r in results:
        results_dict_list.append(result2dict(r))
    print("Results: {}".format(len(results)))
    return results_dict_list
