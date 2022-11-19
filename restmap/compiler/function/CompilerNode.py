from dataclasses import dataclass
from typing import List
from jinja2 import Environment

@dataclass 
class CompilerNode:
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
    
    def compile(self):
        """
        Traverse the generated compilation tree and resolve each element
        given its own parameters and the neighborhoud of its parent and
        children.

        #TODO: Update to 'compile' each nested structure up to its 'enclosing elements' which 
        * A node containing embedded children, should resolve them and return a total value
        * 
        """
        if self._is_enclosing:
            # Needs to first compile its children before it can return its final string
            # Iterates over all 
            self._compile_enclosed_nodes()
         
        # Then 
        current_node = self.head
        while current_node:
            if current_node == self.head and not current_node.children:
                # break out when reaching the root node
                return
            if not current_node.children:
                # Reached a leave
                current_node.compile()
                # Remove the child from the parent
                current_node.parent.children = [node for node in current_node.parent.children if node != current_node]
                # go a level up
                current_node = current_node.parent
            else:
                current_node = current_node.children[0]
        else:
            # Doesn't have any children of its own and 
            pass

    def _compile_enclosed_nodes(self):
        pass