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
    """
    Base class for all authentication kinds.
    Define required arguments interface and 
    provide configuration methods.

    Are used in the compilation step to retrieve
    the necessary arguments for the parametrization
    """
    pass
@dataclass
class CredentialsBase:
    token_refresh: str
@dataclass
class CredentialsDefaults:
    pass
@dataclass
class CredentialsAuthenticator(CredentialsDefaults, AuthenticatorNode, CredentialsBase):
    """
    Authenticates through a token
    """
# TODO Token refresh
     
    def refresh_token(self):
        """Configure token refresh process"""
        pass

