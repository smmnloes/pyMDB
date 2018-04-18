from sqlalchemy import Index

from App.AppMain import db


class Basics(db.Model):
    __tablename__ = 'basics'
    tid = db.Column(db.Integer, primary_key=True)
    primaryTitle = db.Column(db.Text)
    year = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.Text)
    title_nomalized = db.Column(db.Text)


Index('idx_basics', Basics.title_nomalized, Basics.tid, unique=True)


class Ratings(db.Model):
    __tablename__ = 'ratings'
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    averageRating = db.Column(db.REAL)
    numVotes = db.Column(db.Integer)


Index('idx_ratings', Ratings.tid, Ratings.averageRating, unique=True)


class Principals(db.Model):
    __tablename__ = 'principals'
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Integer, db.ForeignKey('names.nid'), primary_key=True)


Index('idx_principals', Principals.tid, Principals.nid, unique=True)


class Writers(db.Model):
    __tablename__ = 'writers'
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Integer, db.ForeignKey('names.nid'), primary_key=True)


Index('idx_writers', Writers.tid, Writers.nid, unique=True)


class Directors(db.Model):
    __tablename__ = 'directors'
    tid = db.Column(db.Integer, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Integer, db.ForeignKey('names.nid'), primary_key=True)


Index('idx_directors', Directors.tid, Directors.nid, unique=True)


class Names(db.Model):
    __tablename__ = 'names'
    nid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    name_normalized = db.Column(db.Text)


Index('idx_names', Names.nid, Names.name_normalized, unique=True)
