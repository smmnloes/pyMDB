from sqlalchemy import Index

from app.app_main import db
from constants.constants import TABLE_BASICS, TABLE_RATINGS, TABLE_PRINCIPALS, INDEX_PREFIX, TABLE_WRITERS, \
    TABLE_DIRECTORS, TABLE_NAMES


class Basics(db.Model):
    __bind_key__ = 'movies'
    __tablename__ = TABLE_BASICS
    tid = db.Column(db.Integer, primary_key=True)
    primaryTitle = db.Column(db.Text)
    year = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.Text)


class Ratings(db.Model):
    __bind_key__ = 'movies'
    __tablename__ = TABLE_RATINGS
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    averageRating = db.Column(db.REAL)
    numVotes = db.Column(db.Integer)


class Principals(db.Model):
    __bind_key__ = 'movies'
    __tablename__ = TABLE_PRINCIPALS
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Integer, db.ForeignKey('names.nid'), primary_key=True)


Index(INDEX_PREFIX + TABLE_PRINCIPALS, Principals.nid, Principals.tid)


class Writers(db.Model):
    __bind_key__ = 'movies'
    __tablename__ = TABLE_WRITERS
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Integer, db.ForeignKey('names.nid'), primary_key=True)


Index(INDEX_PREFIX + TABLE_WRITERS, Writers.nid)


class Directors(db.Model):
    __bind_key__ = 'movies'
    __tablename__ = TABLE_DIRECTORS
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Integer, db.ForeignKey('names.nid'), primary_key=True)


Index(INDEX_PREFIX + TABLE_DIRECTORS, Directors.nid)


class Names(db.Model):
    __bind_key__ = 'movies'
    __tablename__ = TABLE_NAMES
    nid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    name_normalized = db.Column(db.Text)


Index(INDEX_PREFIX + TABLE_NAMES, Names.name_normalized, Names.name)
