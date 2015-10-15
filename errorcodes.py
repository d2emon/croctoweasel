NO_ERROR = {"errcode": 0, "error": "No error"}
ERROR_UNKNOWN = {"errcode": 1, "error": "Unknown error"}
ERROR_ACTION = {"errcode": 2, "error": "Wrong action"}
ERROR_CODE = {"errcode": 3, "error": "Wrong code"}

ERRORS = (
    NO_ERROR,
    ERROR_UNKNOWN,
    ERROR_ACTION,
    ERROR_CODE
)

class WrongCodeError(Exception):
    '''raise this when there is no such user'''
