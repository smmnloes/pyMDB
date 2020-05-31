from sqlalchemy import Index

from app.app_main import db

INDEX_PREFIX = '_idx_'
TABLE_BASICS = 'basics'
TABLE_RATINGS = 'ratings'
TABLE_PRINCIPALS = 'principals'
TABLE_WRITERS = 'writers'
TABLE_DIRECTORS = 'directors'
TABLE_NAMES = 'names'
TABLE_AKAS = 'akas'
TABLE_FTS = 'fts_table'


class Basics(db.Model):
    __tablename__ = TABLE_BASICS
    tid = db.Column(db.Integer, primary_key=True)
    primaryTitle = db.Column(db.Text)
    year = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.Text)


class Ratings(db.Model):
    __tablename__ = TABLE_RATINGS
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    averageRating = db.Column(db.REAL)
    numVotes = db.Column(db.Integer)


class Principals(db.Model):
    __tablename__ = TABLE_PRINCIPALS
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Integer, db.ForeignKey('names.nid'), primary_key=True)


Index(INDEX_PREFIX + TABLE_PRINCIPALS, Principals.nid, Principals.tid)


class Writers(db.Model):
    __tablename__ = TABLE_WRITERS
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Integer, db.ForeignKey('names.nid'), primary_key=True)


Index(INDEX_PREFIX + TABLE_WRITERS, Writers.nid)


class Directors(db.Model):
    __tablename__ = TABLE_DIRECTORS
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Integer, db.ForeignKey('names.nid'), primary_key=True)


Index(INDEX_PREFIX + TABLE_DIRECTORS, Directors.nid)


class Names(db.Model):
    __tablename__ = TABLE_NAMES
    nid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    name_normalized = db.Column(db.Text)


Index(INDEX_PREFIX + TABLE_NAMES, Names.name_normalized, Names.name)
