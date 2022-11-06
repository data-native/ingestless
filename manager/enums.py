from enum import Enum, auto
from manager.types import FunctionItem, ScheduleItem, TriggerItem

# Supported Providers
class RequestModels(Enum):
    FUNCTION = FunctionItem
    SCHEDULE = ScheduleItem
    TRIGGER = TriggerItem

class Provider(Enum):
    AWS = 1
    AZURE = 2
    GCP = 3
    CLOUDNATIVE = 4

# StatusCodes used to communicate results


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

class Services(Enum):
    """
    List of services orchestrated across backend providers.
    
    Each service provider must implement a mapping dictionary,
    to place the correct native service in relation to the general
    service description used here. 
    """
    Function = auto()
    StateMachine = auto()
    ServiceBus = auto()
