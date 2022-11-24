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
    
    def compile_code(self):
        """
        Body Parser compiles the body parsing logic
        into the file
        """
        return self._render_template() 
        