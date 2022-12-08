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
    """
    Defines the available behaviour of response body parsing
    within the function handlers.

    * 
    """
    
    def compile_code(self):
        """
        Body Parser compiles the body parsing logic
        into the file
        """
        template_params = {

        }
        # if self.node.params:
            # TODO Implement parameter resolution in the function
            # template_params['params'] = {param.name: param.resolver.name for param in node.params}

        return self._render_template(template_params) 
        