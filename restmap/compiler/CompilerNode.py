from dataclasses import dataclass
from typing import List
from jinja2 import Environment

@dataclass 
class CompilerNode:
    """
    Inheritance root for the CompilerNodes utilizes
    within the CompilationGraph
    """
    _env: Environment
    _template: str
    _parent: 'CompilerNode'
    _children: List['CompilerNode']
    _code: str = ""
    _is_enclosing: bool = False

    def child(self, node: 'CompilerNode'):
        self._children.append(node)
        self._is_enclosing = True

    def sibbling(self, node: 'CompilerNode'):
        self._parent.child(node)
        self._parent._is_enclosing = True
    
    def compile(self, node: 'CompilerNode'=None) -> str:
        """
        Traverse the generated compilation tree and resolve each element
        given its own parameters and the neighborhoud of its parent and
        children.

        #TODO: Update to 'compile' each nested structure up to its 'enclosing elements' which 
        * A node containing embedded children, should resolve them and return a total value
        * A single node should compile itself and return 
        """
        node = node or self
        if node._is_enclosing:
            # Collect return from component registration
            # Needs to first compile its children before it can return its final string
            for child in node._children:
                self._code += child.compile_code()
                self._children = [node for node in self._children if node != child]
        self._code += self.compile_code()
        return self._code 

    def _render_template(self, arg_dict: dict=None) -> str:
        """
        Renders the code template
        """
        arg_dict = arg_dict or {k: v for k,v in self.__dict__.items() if not k.startswith('_')}
        # TODO Enhace passing of an instance that validated the required dict keys are present
        # assert isinstance(arg_dict, dict)
        template = self._env.get_template(self._template)
        return template.render(arg_dict)

    def compile_code(self):
        """
        Implements the code compilation for that specific node
        """
        raise NotImplementedError