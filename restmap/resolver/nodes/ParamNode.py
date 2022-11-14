from dataclasses import dataclass
from .BaseNode import BaseNode
from .ResolverNode import ResolverNode

@dataclass
class ParamNode(BaseNode):
    name: str
    type: str
    resolver: ResolverNode

