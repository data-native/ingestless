from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode

@dataclass
class BodyParserNodeBase:
    pass
    
@dataclass
class BodyParserNodeDefaults:
    pass

@dataclass
class BodyParserNode(BodyParserNodeDefaults, CompilerNode, BodyParserNodeBase):
    
    def compile(self):

        return 'test' 
        
    def _compile_enclosed_nodes(self):
        raise NotImplementedError