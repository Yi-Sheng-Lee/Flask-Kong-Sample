from enum import Enum


class BaseDaoError(Enum):
    DATA_NOT_FOUND = "DE50001"
    DATA_EXISTED = "DE50002"
    DATA_NULL = "DE50003"
    DATA_TOO_LONG = "DE50004"
    DATA_IN_USE = "DE50005"
