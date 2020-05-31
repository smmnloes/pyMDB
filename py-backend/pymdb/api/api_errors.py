from werkzeug.exceptions import HTTPException

rest_api_errors = {
    'DetailedDataNotFound': {
        'message': "Detailed Data not found for this id!",
        'status': 404,
    },
    'NoTmdbApiKeySpecified': {
        'message': "No TMDB API access key defined, detailed data is not available!",
        'status': 404,
    }
}


class DetailedDataNotFound(HTTPException):
    pass


class NoTmdbApiKeySpecified(HTTPException):
    pass
