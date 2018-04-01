from App.AppMain import db, create_app

app = create_app()
app.app_context().push()


class Basics(db.Model):
    __tablename__ = 'basics'
    tid = db.Column(db.Text, primary_key=True)
    primaryTitle = db.Column(db.Text)
    year = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.Text)


class Ratings(db.Model):
    __tablename__ = 'ratings'
    tid = db.Column(db.Text, primary_key=True)
    averageRating = db.Column(db.REAL)
    numVotes = db.Column(db.Integer)


class Principals(db.Model):
    __tablename__ = 'principals'
    tid = db.Column(db.Text, primary_key=True)
    nid = db.Column(db.Text, primary_key=True)
    category = db.Column(db.Text, primary_key=True)
    characters = db.Column(db.Text, primary_key=True)


class Writers(db.Model):
    __tablename__ = 'writers'
    tid = db.Column(db.Text, primary_key=True)
    nid = db.Column(db.Text, primary_key=True, index=True)


class Directors(db.Model):
    __tablename__ = 'directors'
    tid = db.Column(db.Text, primary_key=True)
    nid = db.Column(db.Text, primary_key=True, index=True)


class Names(db.Model):
    __tablename__ = 'names'
    nid = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, index=True)