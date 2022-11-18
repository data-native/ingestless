from dataclasses import dataclass
from .Compiler import CompilerNode

@dataclass
class HandlerNodeBase:
    timeout: int

@dataclass
class HandlerNodeDefaults:
    retry: int = 3

@dataclass
class HandlerNode(HandlerNodeDefaults, CompilerNode, HandlerNodeBase):


    def compile(self) -> str:
        """
        The overall handler code structure
        
        Can resolve elements within its body.
        """
        pass