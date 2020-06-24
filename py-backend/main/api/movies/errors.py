from werkzeug.exceptions import HTTPException


class DetailedDataNotFound(HTTPException):
    message = 'Detailed Data not found for this id'
    status = 404


class NoTmdbApiKeySpecified(HTTPException):
    message = 'No TMDB API access key defined, detailed data is not available'
    status = 404


movie_api_errors = {
    DetailedDataNotFound.__name__: {
        'message': DetailedDataNotFound.message,
        'status': DetailedDataNotFound.status,
    },
    NoTmdbApiKeySpecified.__name__: {
        'message': NoTmdbApiKeySpecified.message,
        'status': NoTmdbApiKeySpecified.status,
    }
}
