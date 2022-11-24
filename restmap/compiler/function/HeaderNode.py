from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode

@dataclass
class HeaderNodeBase:
    pass
    
@dataclass
class HeaderNodeDefaults:
    UserAgent: str = "TestAgent: Chrome"
    Accept: str = "text/html, application/json"
    AcceptLanguage: str = 'en-US'
    cache_max_age = "cache-max-age=0"

@dataclass
class HeaderNode(HeaderNodeDefaults, CompilerNode, HeaderNodeBase):

    def compile_code(self) -> str:
        """
        The header configuration is compiled 
        based on the parametrization of the request template
        
        return: A configuration dict passed 
        """
        # Retrieve the list of parameters set on the inh
        
        # Call the set of functions to generate the code
        return self._render_template()
    
    
