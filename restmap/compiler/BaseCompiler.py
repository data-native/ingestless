from pathlib import Path
from jinja2 import Environment, PackageLoader
from restmap.compiler.CompilerNode import CompilerNode 

class BaseCompiler:
    """
    Inheritance base for the Constructor specific compilation classes

    Each specific compiler contains the logic to create the required 
    set of compilation nodes for their target serverless service.

    Constructors supported
    -------------------------
    >>> from .function import FunctionCompiler
    >>> func_compiler = FunctionCompiler.FunctionCompiler() 
    >>> assert isinstance(func_compiler, BaseCompiler)
    """

    def __init__(self, compilation_dir:str='./ingestless/restmap/src') -> None:
        env = Environment(loader=PackageLoader("restmap", "compiler/templates"))
        self.env = env 
        self.head = CompilerNode(
            _env=env, 
            _template=None, 
            _parent=None, 
            _children=[])
        self.output_location = Path(compilation_dir)

    # TODO: Generalize the compiler to accept a language parameter and load the templates accordingly
    def compile(self):
        """
        Performs a traversal on the compilation graph 
        to resolve nested subtrees and the overall tree
        to create the final code output.
        """ 
        # TODO Resolve subtrees in 'enclosing nodes'
         
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

        