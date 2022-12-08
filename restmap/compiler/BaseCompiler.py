from pathlib import Path
from jinja2 import Environment, PackageLoader
from typing import List
from enums import Constructs
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.compiler.CompilerNode import CompilerNode 
# from restmap.orchestrator.OrchestrationGraph import OrchestrationNode

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
        self._selected_head: CompilerNode = None
     
    # TODO: Generalize the compiler to accept a language parameter and load the templates accordingly
    def compile(self, graph: ResolutionGraph):
        """
        Performs a traversal on the compilation graph 
        to resolve nested subtrees and the overall tree
        to create the final code output.
        """ 
        pass
    
    def use(self, node, compiler:'BaseCompiler'=None) -> 'BaseCompiler':
        """
        Sets the compilation graph for the given `OrchestrationNode`
        to allow adapatations to the code compilation during later
        stages of the execution process. 
        """
        return CompilationContextProvider(
            compiler=compiler or self,
            # kind='function', # TODO Check if this needs to be adapted
            selected_construct=node.name
        )
    
    def set_active(self, head: CompilerNode):
        """Sets the given head as the current scope"""    
        assert isinstance(head, CompilerNode)
        self._selected_head = head

class CompilationContextProvider:

    def __init__(self,
        compiler: BaseCompiler,
        selected_construct: str
    ) -> None:
        self.compiler = compiler
        self.selected_construct = selected_construct

    def __enter__(self) -> BaseCompiler:
        try:
            # Identify the correct starting head
            head = self.compiler._head_registry[self.selected_construct]
            self.compiler.set_active(head=head)
            return self.compiler
        except KeyError:
            raise KeyError(f"No construct {self.selected_construct} registered. If configured, register the function with the Provider first.") 

    def __exit__(self, exception_type, exception_value, traceback):
        self.compiler._selected_head = None
