from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode

@dataclass
class HeaderNodeBase:
    pass
    
@dataclass
class HeaderNodeDefaults:
    agent: str = "TestAgent: Chrome"

@dataclass
class HeaderNode(CompilerNode):

    def compile(self) -> str:
        """
        The header 
        """
        pass

