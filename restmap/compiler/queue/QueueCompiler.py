
"""

"""
# TODO Add Doc on communication between compiler and construct compiler
from typing import Union, List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass

from restmap.resolver.ResolutionGraph import ResolutionGraph
# Might not need any code compilation, just logical execution 
# from restmap.compiler.queue import HandlerNode, HeaderNode, RequestNode, BodyParserNode
from restmap.compiler.BaseCompiler import BaseCompiler
from restmap.compiler.CompilerNode import CompilerNode


# FUNCTION_COMPILER__________________________
@dataclass
class DeploymentParams:
    """
    Standard set of parameters to configure the deployment
    of the serverless function on the BackendProvider

    Represents the function service contract to be implemented
    by the Backend Provider
    """

    # TODO Define the abstraction parameters for the queue object

    pass


@dataclass
class QueueDeployment:
    """
    The compilation output that can be send to the 
    BackendProvider for function deployment
    
    Defines the contract between `Compiler` and `BackendProvider`
    """
    uid : str = ''
    is_deployed: bool = False

class QueueCompiler(BaseCompiler):
    """
    Compiles business logic
     
    Can add elements to the graph.
    Can iterate over the parse tree and compile the code.
    Tree structure allows the nodes to take their context
    into account when creating code fragments.
    """
    def __init__(self, 
        compiler: BaseCompiler, #Actually the parent Compiler. Used to access the other compiler to request resource allocation dynamically
        compilation_dir: str='./ingestless/restmap/src', 
        language:str="Python@3.9",

        ) -> None:
        super().__init__(compilation_dir)

    def compile(self, head: CompilerNode, function: ResolutionGraph) -> QueueDeployment:
        """
        Compiles 
        """
        # TODO Implement the attribution logic based on set parameters 
        deployment_params = self._compile_params()

        return QueueDeployment(
            uid=function.name,
        )

    def _append_to_parent(self, parent: CompilerNode, node: CompilerNode):
        """Appends to given parent, or else to Compilation Tree root"""
        parent.child(node) 


