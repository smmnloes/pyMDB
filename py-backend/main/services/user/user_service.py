from datetime import datetime

import jwt
from email_validator import validate_email, EmailNotValidError
from flask import make_response, jsonify

from api.user.errors import UserEmailExistsException, UserNameExistsException, EmailNotValidException, \
    LoginFailedException
from app import app_main
from constants import constants
from model.user_model import User
from services.config import config_service


def check_email_exists(email):
    if User.query.filter(User.email == email).first():
        raise UserEmailExistsException


def check_username_exists(username):
    if User.query.filter(User.username == username).first():
        raise UserNameExistsException


def get_email_normalized(email):
    """
    Check if email is valid. Return normalized form if it is valid, otherwise none
    """
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError as e:
        return None


def register_user(email, password, username, admin=False):
    check_username_exists(username)
    check_email_exists(email)

    email_normalized = get_email_normalized(email)
    if not email_normalized:
        raise EmailNotValidException

    user = User(
        email, password, username, admin
    )
    app_main.db.session.add(user)
    app_main.db.session.commit()


def login_user(email, password):
    user = User.query.filter_by(
        email=email
    ).first()

    if (not user) or (not app_main.bcrypt.check_password_hash(user.password, password)):
        raise LoginFailedException

    auth_token = encode_auth_token(user.id)
    response_object = {
        'status': 'success',
        'message': 'Successfully logged in.',
        'auth_token': auth_token.decode()
    }
    return make_response(jsonify(response_object), 200)


def encode_auth_token(user_id):
    payload = {
        'exp': datetime.utcnow() + constants.JWT_VALIDITY_PERIOD,
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        config_service.get_app_key(),
        algorithm='HS256'
    )


def decode_auth_token(auth_token):
    """
    :param auth_token:
    :return:
    :raises:    jwt.ExpiredSignatureError if token expired
                jwt.InvalidTokenError if token invalid
    """
    payload = jwt.decode(auth_token, config_service.get_app_key())
    return payload['sub']
