from flask import Flask


def create_test_app(DB_PATH):
    test_app = Flask(__name__)
    test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
    return test_app
