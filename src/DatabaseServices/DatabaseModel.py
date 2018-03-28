from AppMain import db


class Basics(db.Model):
    tid = db.Column(db.Text, primary_key=True)
    primaryTitle = db.Column(db.Text)
    year = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.Text)


class Ratings(db.Model):
    tid = db.Column(db.Text, db.ForeignKey('basics.tid'))
    averageRating = db.Column(db.REAL)
    numVotes = db.Column(db.Integer)


class Principals(db.Model):
    tid = db.Column(db.Text, db.ForeignKey('basics.tid'))
    nid = db.Column(db.Text, db.ForeignKey('names.nid'))
    category = db.Column(db.Text)
    characters = db.Column(db.Text)


class Writers(db.Model):
    tid = db.Column(db.Text, db.ForeignKey('basics.tid'))
    nid = db.Column(db.Text, db.ForeignKey('names.nid'))


class Directors(db.Model):
    tid = db.Column(db.Text, db.ForeignKey('basics.tid'))
    nid = db.Column(db.Text, db.ForeignKey('names.nid'))


class Names(db.Model):
    nid = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)


class Akas(db.Model):
    tid = db.Column(db.Text)
    title = db.Column(db.Text)
