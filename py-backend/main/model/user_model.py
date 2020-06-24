from datetime import datetime

from flask_bcrypt import Bcrypt

from app.app_main import db
from constants.constants import BIND_USERS


class User(db.Model):
    __bind_key__ = BIND_USERS
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, username, admin=False):
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(
            password
        ).decode('utf-8')
        self.admin = admin


class BlacklistToken(db.Model):
    __bind_key__ = BIND_USERS
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()