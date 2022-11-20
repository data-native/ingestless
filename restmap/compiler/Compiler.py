"""


"""
from enums import Constructs
from restmap.compiler.BaseCompiler import BaseCompiler
from restmap.resolver.ResolutionGraph import ResolutionGraph

from restmap.compiler.function.FunctionCompiler import FunctionCompiler


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
        self._function_compiler = FunctionCompiler()
    
    def from_resolution_graph(self, graph: ResolutionGraph):
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
      
    def _compile_endpoint(self, graph: ResolutionGraph):
      """
      Compile the endpoint schema
      * All resolvers need to be compiled to executable functionsSD The dependencies between the functions need to be passed to the orchestrator
      
      """
      # Endpoints contain one or multiple endpoints
      # All resolvers neeed to run for this endpoint to resolve
      for resolver in graph._resolvers:
        # The resolution should adapt 
        self._compile_resolver(resolver)
      for endpoint in graph._endpoints:
        self._compile_endpoint(endpoint)
      # They can contain a base and a relative  
      
        
    def _compile_resolver(self, resolver_graph: ResolutionGraph):
      """Compile the endpoint schema"""
      from restmap.compiler.function.FunctionCompiler import FunctionResolutionSubgraph
      # TODO Needs to cache/retrieve previously compiled resolvers when they are referenced multiple times
      # TODO A resolver mentioned in a parameter/endpoint node indicates that after compilation, the orchestrator needs to schedule a dependency

      # Resolvers can be of various types 
      
      # They can optionally contain parameters 
      if resolver_graph._params:
        # Parameters must also be resolved
        for param in resolver_graph._params: 
          # If the param requires a resolver (e.g. not a shared variable)
          if param._resolver:
            # Recursively resolve the resolver
            # TODO Resolved value must be available within this context to resolve the overall parametrization for the endpoint
            param_val = self._compile_resolver(param._resolver)
          else:
            # Compile the param node to retrieve the value
            param_val = param.compile()
      # After this point all parameters should be resolved within the scope
      # Now create the resolver as a function
      function_graph = FunctionResolutionSubgraph(resolver_graph)
      function_deployment = self._function_compiler.compile(function_graph)
      # Returns a configuration class capable of instructing the provider Backend to deploy a function
      return function_deployment

