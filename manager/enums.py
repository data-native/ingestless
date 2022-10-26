from enum import Enum, auto

class StatusCode(Enum):
    SUCCESS = auto()
    DIR_ERROR = auto()
    FILE_ERROR = auto()
    DB_READ_ERROR = auto()
    DB_WRITE_ERROR = auto()
    JSON_ERROR = auto()
    ID_ERROR = auto()

# Define error messages for all errorCodes
Errors = {
    StatusCode.DIR_ERROR: "config dir error",
    StatusCode.FILE_ERROR: "config file error",
    StatusCode.DB_READ_ERROR: "database read error",
    StatusCode.DB_WRITE_ERROR: "database write error",
}