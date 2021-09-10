from enum import Enum

class ErrorCode(Enum):
    FIELD_ERROR = 'HIERR1001'

    #Security Error Codes
    TOKEN_INVALID = 'HIERR2001'
    TOKEN_MISSING = 'HIERR2002'
    NO_AUTHORIZATION = 'HIERR2003'

    GENERIC_ERROR = 'HIERR3001'

    NO_DOCUMENT = 'HIERR4001'

    INVALID_COORDINATES = 'HIERR5001'