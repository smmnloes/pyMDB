from App.AppMain import db


class Basics(db.Model):
    __tablename__ = 'basics'
    tid = db.Column(db.Text, primary_key=True)
    primaryTitle = db.Column(db.Text)
    year = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.Text)


class Ratings(db.Model):
    __tablename__ = 'ratings'
    tid = db.Column(db.Text, db.ForeignKey('basics.tid'), primary_key=True)
    averageRating = db.Column(db.REAL)
    numVotes = db.Column(db.Integer)


class Principals(db.Model):
    __tablename__ = 'principals'
    rowid = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Text, db.ForeignKey('basics.tid'))
    nid = db.Column(db.Text, db.ForeignKey('names.nid'))
    category = db.Column(db.Text)
    characters = db.Column(db.Text)


class Writers(db.Model):
    __tablename__ = 'writers'
    tid = db.Column(db.Text, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Text, db.ForeignKey('names.nid'), primary_key=True, index=True)


class Directors(db.Model):
    __tablename__ = 'directors'
    tid = db.Column(db.Text, db.ForeignKey('basics.tid'), primary_key=True)
    nid = db.Column(db.Text, db.ForeignKey('names.nid'), primary_key=True, index=True)


class Names(db.Model):
    __tablename__ = 'names'
    nid = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, index=True)
