from pathlib import Path
from jinja2 import Environment, PackageLoader
from typing import List
from enums import Constructs
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.compiler.CompilerNode import CompilerNode 

#TODO Extend this to ABC
class BaseCompiler:
    """
    Inheritance base for the Constructor specific compilation classes

    Each specific compiler contains the logic to create the required 
    set of compilation nodes for their target serverless service.

    """

    def __init__(self, compilation_dir:str='./ingestless/restmap/src') -> None:
        env = Environment(loader=PackageLoader("restmap", "compiler/templates"))
        self.env = env 
        self.heads = []
        self.output_location = Path(compilation_dir)

    # TODO: Generalize the compiler to accept a language parameter and load the templates accordingly
    def compile(self, graph: ResolutionGraph):
        """
        Performs a traversal on the compilation graph 
        to resolve nested subtrees and the overall tree
        to create the final code output.
        """ 
        pass
        # TODO Resolve subtrees in 'enclosing nodes'
         
        # TODO Enable this traversal to receive a selected head endpoint 
        # current_node = head 
        # while current_node:
            # if current_node == self.heads and not current_node.children:
                # break out when reaching the root node
                # return
            # if not current_node.children:
                # Reached a leave
                # current_node.compile()
                # Remove the child from the parent
                # current_node.parent.children = [node for node in current_node.parent.children if node != current_node]
                # go a level up
                # current_node = current_node.parent
            # else:
                # current_node = current_node.children[0]
        # else:
            # Doesn't have any children of its own and 
            # pass

