from enum import Enum


class HttpCodeEnum(Enum):
    ENDPOINT_NOT_FOUND = "CE40400"
    METHOD_NOT_ALLOWED = "CE40500"
    INTERNAL_SERVER_ERROR = "CE50000"
