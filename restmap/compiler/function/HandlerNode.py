from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode


@dataclass
class HandlerNodeBase:
    _template: str
@dataclass
class HandlerNodeDefaults:
    timeout: int = 500
    retry: int = 3

@dataclass
class HandlerNode(HandlerNodeDefaults, CompilerNode, HandlerNodeBase):
    """
    Compiles the request handler configuration for function integration
    """

    def compile_code(self) -> str:
        """
        The overall handler code structure
        
        Can resolve elements within its body.
        """
        # Load template
        # template = self._env.get_template(self._template)
        # Compile template wth parameters
        # param_dict = {k: self.__dict__[k] for k in self.__dict__.keys() if not k.startswith('_')} 
        # return template.render(**param_dict
        return self._render_template()