from datetime import datetime

import jwt
from email_validator import validate_email, EmailNotValidError
from flask import make_response, jsonify
from flask_bcrypt import Bcrypt

from api.user.errors import UserEmailExistsException, UserNameExistsException, EmailNotValidException, \
    LoginFailedException, NoTokenProvidedException, TokenExpiredException, TokenBlacklistedException
from app import app_main
from constants import constants
from model.user_model import User, BlacklistToken
from services.config import config_service


def check_email_exists(email):
    if User.query.filter(User.email == email).first():
        raise UserEmailExistsException


def check_username_exists(username):
    if User.query.filter(User.username == username).first():
        raise UserNameExistsException


def get_email_normalized(email):
    """
    Check if email is valid. Return normalized form if it is valid, otherwise None
    """
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError:
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
    auth_token = encode_auth_token(user.id)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.',
        'auth_token': auth_token.decode()
    }
    return make_response(jsonify(response_object), 201)


def login_user(email, password):
    user = User.query.filter_by(
        email=get_email_normalized(email)
    ).first()

    if (not user) or (not Bcrypt().check_password_hash(user.password, password)):
        raise LoginFailedException

    auth_token = encode_auth_token(user.id)
    response_object = {
        'status': 'success',
        'message': 'Successfully logged in.',
        'auth_token': auth_token.decode()
    }
    return make_response(jsonify(response_object), 200)


def logout_user(request):
    auth_token = get_token_from_request(request)
    decode_auth_token(auth_token)
    blacklist_token(auth_token)
    app_main.db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return make_response(jsonify(response_object), 200)


def blacklist_token(token):
    app_main.db.session.add(BlacklistToken(token))
    app_main.db.session.commit()


def is_blacklisted(auth_token):
    return BlacklistToken.query.filter(BlacklistToken.token == auth_token).first() is not None


def get_token_from_request(request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None
    if not auth_token:
        raise NoTokenProvidedException
    return auth_token


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
    :param auth_token: encoded token
    :return: the subject identity that is contained in the token
    :raises:    jwt.ExpiredSignatureError if token expired
                jwt.InvalidTokenError if token invalid
    """
    if is_blacklisted(auth_token):
        raise TokenBlacklistedException
    try:
        payload = jwt.decode(auth_token, config_service.get_app_key())
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    except jwt.InvalidTokenError:
        raise NoTokenProvidedException
