"""


"""
from typing import List
from enums import Constructs
from restmap.compiler.BaseCompiler import BaseCompiler
from restmap.resolver.ResolutionGraph import ResolutionGraph
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
        self._function_compiler = FunctionCompiler()
    
    def from_resolution_graph(self, graph: ResolutionGraph) -> List[FunctionDeployment]:
        """
        Traverses the resolution graph to compile the required components
        using the logic implemented in the resource Compiler classes.

        Each construct compiler is maintaining the required node types
        and configuration logic to create and resolve the required compilation
        steps to handle the conditional code and infrastructure creation based 
        on the ResolutionGraph components.
        """
        # Switch on selected templates
        #TODO Resolver must parse kind:str to Construct Enum when resolving the ResolutionGraph 
        kind_switch: dict[Constructs, BaseCompiler] = {
            Constructs.Endpoint : self._compile_endpoint,
            Constructs.Resolver : self._compile_resolver,
        }
        
        # Routes the template to the compilation method based on kind
        compilation_result = kind_switch[graph.kind](graph)
        return compilation_result
      
    def _spawn_head(self) -> CompilerNode:
        """
        Starts a new parallel compilation tree head
        
        This enables the Compiler to compile multiple functions within 
        a given compilation process.
        """
        head = CompilerNode(
            _env = self.env,
            _template = '',
            _parent = None,
            _children = [], 
            _code= '',
            _is_enclosing = True
        )
        self.heads.append(head)
        return head

    def _compile_endpoint(self, graph: ResolutionGraph) -> List[FunctionDeployment]:
      """
      Compile the endpoint schema
      * All resolvers need to be compiled to executable functionsSD The dependencies between the functions need to be passed to the orchestrator
      
      """
      compiled_function_requests = [] 
      # Endpoints contain one or multiple endpoints
      for endpoint in graph._endpoints:
        head = self._spawn_head()
        # Want to retain the dependency graph
        compiled_function_requests.append(self._function_compiler.compile(head, endpoint)) 

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

