from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode 

@dataclass
class ResponseHandlerBase:
    pass

@dataclass
class ResponseHandlerDefaults:
    pass

@dataclass
class ResponseHandlerNode(ResponseHandlerDefaults, CompilerNode , ResponseHandlerBase):
    """
    Handles the compilation of response handler logic
    """

    def compile_code(self):
        return "<<Response Handler>>"