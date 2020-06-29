from werkzeug.exceptions import HTTPException


class UserEmailExistsException(HTTPException):
    message = 'Email address already registered'
    status = 400


class UserNameExistsException(HTTPException):
    message = 'Username already registered'
    status = 400


class EmailNotValidException(HTTPException):
    message = 'Email address not valid'
    status = 400


class LoginFailedException(HTTPException):
    message = 'Username or password incorrect'
    status = 400


class NoTokenProvidedException(HTTPException):
    message = 'Please provide valid auth token'
    status = 400


class TokenExpiredException(HTTPException):
    message = 'Token has expired'
    status = 400


class TokenBlacklistedException(HTTPException):
    message = 'Token is blacklisted'
    status = 400


class UnauthorizedException(HTTPException):
    message = 'Authorization required. Please log in'
    status = 401


class UserNameInvalidException(HTTPException):
    message = 'Invalid username'
    status = 400


class PasswordInvalidException(HTTPException):
    message = 'Invalid password'
    status = 400


user_api_errors = {
    UserEmailExistsException.__name__: {
        'message': UserEmailExistsException.message,
        'status': UserEmailExistsException.status
    },
    UserNameExistsException.__name__: {
        'message': UserNameExistsException.message,
        'status': UserNameExistsException.status
    },
    EmailNotValidException.__name__: {
        'message': EmailNotValidException.message,
        'status': EmailNotValidException.status
    },
    LoginFailedException.__name__: {
        'message': LoginFailedException.message,
        'status': LoginFailedException.status
    },
    NoTokenProvidedException.__name__: {
        'message': NoTokenProvidedException.message,
        'status': NoTokenProvidedException.status
    },
    TokenExpiredException.__name__: {
        'message': TokenExpiredException.message,
        'status': TokenExpiredException.status
    },
    TokenBlacklistedException.__name__: {
        'message': TokenBlacklistedException.message,
        'status': TokenBlacklistedException.status
    },
    UnauthorizedException.__name__: {
        'message': UnauthorizedException.message,
        'status': UnauthorizedException.status
    },
    UserNameInvalidException.__name__: {
        'message': UserNameInvalidException.message,
        'status': UserNameInvalidException.status
    },
    PasswordInvalidException.__name__: {
        'message': PasswordInvalidException.message,
        'status': PasswordInvalidException.status
    }

}
