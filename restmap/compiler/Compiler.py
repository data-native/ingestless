"""


"""
from pathlib import Path
from typing import List, Dict
from enums import Constructs
from restmap.compiler.BaseCompiler import BaseCompiler
from restmap.orchestrator.OrchestrationGraph import OrchestrationGraph
from restmap.resolver.nodes.resolvers import ResolverNode

from restmap.compiler.function.FunctionCompiler import FunctionCompiler, FunctionCompilationRequest, FunctionDeployment
from restmap.compiler.CompilerNode import CompilerNode

class Compiler(BaseCompiler):
    """
    Implements the management interface to the Compilation process
    across all supported construct Compiler.

    * Routes incoming compilation requests across all required construct
      specific Compiler
    * Integrates the results from the individual construct compilers into
      the communication to the BackendProvider
    * Provides the unified management API to the rest of the program, especially
      the Manager to drive compilation processes
    """ 
    def __init__(self, compilation_dir: str = './ingestless/restmap/src') -> None:
        super().__init__(compilation_dir)
        #TODO Enable the compiler to receive a language compiler to select the type of compilation stack to use
        self.heads = []
        self._head_registry = {}
        self.output_location = Path(compilation_dir)
        # Instantiate the construct specific compiler
        self._function_compiler = FunctionCompiler(compiler=self)

    @property
    def function(self):
      return self._function_compiler

    def from_orchestration_graph(self, graph: OrchestrationGraph) -> Dict[str, FunctionDeployment]:
        """
        Traverses the orchestration graph to compile the required components
        using the logic implemented in the resource Compiler classes.

        Each construct compiler is maintaining the required node types
        and configuration logic to create and resolve the required compilation
        steps to handle the conditional code and infrastructure creation based 
        on the ResolutionGraph components.
        """
        #TODO Resolver must parse kind:str to Construct Enum when resolving the ResolutionGraph 
        # kind_switch: dict[Any, BaseCompiler] = {
            # : self._compile_endpoint,
            # : self._compile_resolver,
        # }
        deployables = {}
        # Routes the template to the compilation method based on kind
        for name, node in graph.nodes.items():
          head = self._spawn_head(name)
          compiled_deployable = self._function_compiler.compile(head, node.construct) 
          deployables[name] = compiled_deployable
        return deployables
      
    def _spawn_head(self, name:str) -> CompilerNode:
        """
        Starts a new parallel compilation tree head
        
        This enables the Compiler to compile multiple functions within 
        a given compilation process.
        """
        head = CompilerNode(
            env = self.env,
            template = '',
            parent = None,
            children = [], 
            code= '',
            is_enclosing = True
        )
        self.heads.append(head)
        self._head_registry[name] = head
        return head

    def _compile_endpoint(self, graph: OrchestrationGraph) -> List[FunctionDeployment]:
      """
      Compile the endpoint schema
      * All resolvers need to be compiled to executable functionsSD The dependencies between the functions need to be passed to the orchestrator
      
      """
      compiled_function_requests = [] 
      # Endpoints contain one or multiple endpoints
      for endpoint in graph._endpoints.values():
        head = self._spawn_head()
        # Want to retain the dependency graph
        compiled_function_requests.append(self._function_compiler.compile(head, endpoint)) 
      for resolver in graph._resolvers.values():
        head = self._spawn_head()
        compiled_function_requests.append(self._function_compiler.compile(head, resolver))

      return compiled_function_requests
      
    def _compile_resolver(self, resolver_graph: ResolverNode):
      """
      Compile the resolver configuration to a DeployableFunction
      instance that can be send to the BackendProvider to deploy
      a serverless function for the resolver. 
      """
      # TODO Needs to cache/retrieve previously compiled resolvers when they are referenced multiple times
      # TODO A resolver mentioned in a parameter/endpoint node indicates that after compilation, the orchestrator needs to schedule a dependency

      # Resolvers can be of various types 
      if resolver_graph.kind == 'EndpointResolver':
        # Need to ensure the endpoint mentioned is resolvable
        dependent_resolver = resolver_graph.endpoint
        pass
      elif resolver_graph.kind == 'DBResolver':
        # Needs to create a DB resolution logic in the function
        # Extract the connection str and validate
        # Generate the fully parametrized url
        pass

      # After this point all parameters should be resolved within the scope
      # Now create the resolver as a function
      function_graph = FunctionCompilationRequest(resolver_graph)
      function_deployment = self._function_compiler.compile(function_graph)
      # Returns a configuration class capable of instructing the provider Backend to deploy a function
      return function_deployment

