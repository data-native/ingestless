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

    def compile_code(self) -> str:
        """
        The header configuration is compiled 
        based on the parametrization of the request template
        
        return: A configuration dict passed 
        """
        agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9)"
        response_types_allowed = ','.join(['text/html', 'application/xhtml+xml'])
        response_language_allowed = 'en-US'
        cache_max_age = "cache-max-age=0"
        dict = {
            'User-Agent': agent,
            'Accept': response_types_allowed,
            'Accept-Language': response_language_allowed,
            'Cache-Control': cache_max_age
        }
    
        return "<<HEADER CODE>>"
