from dataclasses import dataclass
from .Compiler import CompilerNode

@dataclass
class HeaderNodeBase:
    pass
    
@dataclass
class HeaderNodeDefaults:
    pass

@dataclass
class RequestNode(CompilerNode):
    pass