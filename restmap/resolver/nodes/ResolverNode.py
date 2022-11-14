from dataclasses import dataclass
from .BaseNode import BaseNode

@dataclass
class ResolverNode(BaseNode):
    """
    A resolver that provides an single or iterable
    value for a given parameter value in other services.
    """
    name: str
