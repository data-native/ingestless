from dataclasses import dataclass
from typing import List
from jinja2 import Environment

@dataclass 
class CompilerNode:
    """
    Inheritance root for the CompilerNodes utilizes
    within the CompilationGraph
    """
    env: Environment
    template: str
    parent: 'CompilerNode'
    children: List['CompilerNode']
    code: str = ""
    is_enclosing: bool = False

    def child(self, node: 'CompilerNode'):
        self.children.append(node)
        self.is_enclosing = True

    def sibbling(self, node: 'CompilerNode'):
        self.parent.child(node)
        self.parent.is_enclosing = True
    
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
        if node.is_enclosing:
            # Collect return from component registration
            # Needs to first compile its children before it can return its final string
            for child in node.children:
                self.code += child.compile_code()
                self.children = [node for node in self.children if node != child]
        self.code += self.compile_code()
        return self.code 

    def _render_template(self, arg_dict: dict=None) -> str:
        """
        Renders the code template
       """
        arg_dict = arg_dict or {k: v for k,v in self.__dict__.items() if not k.startswith('_')}
        # TODO Enhace passing of an instance that validated the required dict keys are present
        # assert isinstance(arg_dict, dict)
        template = self.env.get_template(self.template)
        return template.render(arg_dict)

    def compile_code(self):
        """
        Compile the code template given the parameters
        set on the node instance. 
        """
        # Ensure validity of the configuration
        self._assert_valid_config()
        # Compile template wth parameters
        param_dict = {k: self.__dict__[k] for k in self.__dict__.keys() if not k.startswith('_')} 
        return self._render_template(param_dict)

    def _assert_valid_config(self) -> bool:
        """
        Checks the presence of configuration patters on the compiler
        node. Contains the business logi of configuration patterns that are 
        enabled and reasonable on the code element.
        """
        raise NotImplementedError