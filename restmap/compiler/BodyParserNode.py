from dataclasses import dataclass
from .Compiler import CompilerNode

@dataclass
class BodyParserNodeBase:
    pass
    
@dataclass
class BodyParserNodeDefaults:
    pass

@dataclass
class BodyParserNode(CompilerNode):
    pass
