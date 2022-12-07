"""
Defines Enumerations used within the scope
of the RestMap service.
"""
from enum import Enum, auto

class RestMethod(Enum):
    """
    Supported REST Methods within the framework
    """
    GET = auto()
    PUT = auto()
    POST = auto()
    UPDATE = auto()
    DELETE = auto()