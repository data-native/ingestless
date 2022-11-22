from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode

@dataclass
class AuthenticatorNodeBase:
    pass
    
@dataclass
class AuthenticatorNodeDefaults:
    agent: str = "TestAgent: Chrome"

@dataclass
class AuthenticatorNode(CompilerNode):

    def compile_code(self) -> str:
        """
        Compiles the authentication code 
        """
        pass

