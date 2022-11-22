from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode

@dataclass
class HeaderNodeBase:
    pass
    
@dataclass
class HeaderNodeDefaults:
    pass

@dataclass
class RequestNode(CompilerNode):

    def compile_code(self, node: 'CompilerNode' = None):
        
        return "<<REQUEST HANDLING CODE>>"
