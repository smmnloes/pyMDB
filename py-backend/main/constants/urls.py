from urllib.parse import urljoin

API_ROOT = '/api/'
API_ROOT_MOVIES = urljoin(API_ROOT, 'movies/')
API_ROOT_USER = urljoin(API_ROOT, 'user/')

API_MOVIES_QUERY = urljoin(API_ROOT_MOVIES, 'query')
API_MOVIES_RESULT_COUNT = urljoin(API_ROOT_MOVIES, 'result_count')
API_MOVIES_BY_TID = urljoin(API_ROOT_MOVIES, 'movie_by_tid')
API_MOVIES_DETAILS =  urljoin(API_ROOT_MOVIES, 'details')
API_MOVIES_HAS_DETAILS = urljoin(API_ROOT_MOVIES, 'has_details')

API_USER_REGISTER = urljoin(API_ROOT_USER, 'register')
API_USER_LOGIN = urljoin(API_ROOT_USER, 'login')
API_USER_LOGOUT = urljoin(API_ROOT_USER, 'logout')
API_USER_INFO = urljoin(API_ROOT_USER, 'info')