from flask_bcrypt import generate_password_hash

from app.app_main import db
from constants.constants import BIND_USERS


class User(db.Model):
    __bind_key__ = BIND_USERS
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, username, admin=False):
        self.email = email
        self.username = username
        self.password = generate_password_hash(
            password
        ).decode('utf-8')
        self.admin = admin
