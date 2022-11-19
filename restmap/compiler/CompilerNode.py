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
    code: str = ""
    _is_enclosing: bool = False

    def child(self, node: 'CompilerNode'):
        self._children.append(node)

    def sibbling(self, node: 'CompilerNode'):
        self._parent.child(node)
    
    def compile(self, node: 'CompilerNode'=None):
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
                self.code += self.compile(child)

        self._children = [node for node in self._children if node != child]
        return self.code 


