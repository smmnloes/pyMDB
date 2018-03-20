from flask import current_app
from flask_sqlalchemy import SQLAlchemy

from DatabaseServices import Paths

app = current_app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + Paths.LOCAL_DB
db = SQLAlchemy(app)

