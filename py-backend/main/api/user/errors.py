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
    message = 'Login failed'
    status = 400


user_api_errors = {
    UserEmailExistsException.__name__: {
        'message': UserEmailExistsException.message,
        'status': UserNameExistsException.status
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
    }
}
