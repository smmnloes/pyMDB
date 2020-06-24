from flask import request

from api.user.errors import UnauthorizedException
from services.user.user_service import get_token_from_request, decode_auth_token


def login_required(func):
    def wrapper(*args, **kwargs):
        print("Calling protected route")
        try:
            decode_auth_token(get_token_from_request(request))
        except Exception:
            raise UnauthorizedException

        func(*args, **kwargs)

    return wrapper
