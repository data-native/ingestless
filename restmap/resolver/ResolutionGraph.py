"""

"""
from typing import Dict
from enums import Constructs
from restmap.resolver.nodes import EndpointNode, ParamNode, BaseNode
from restmap.resolver.nodes.resolvers import ResolverNode

class ResolutionGraph:
    """
    The parse graph represents the logical
    dependency resolution amongst the scheduled
    assets in a given endpoint workflow.
    """

    #TODO: Register all elements into execution chains if they are dependent
    #TODO: Ensure iterative execution is enabled on all Nodes
    
    def __init__(self) -> None:
        #TODO: Implement scheduling on multiple 'threads' of depdendency resolution to enable parallel execution
        self._kind = None
        self._head = None
        self._resolvers: Dict[str, ResolverNode.ResolverNode] = {}
        self._params: Dict[str, ParamNode.ParamNode] = {}
        self._endpoints: Dict[str, EndpointNode.EndpointNode] = {}

    # PROPERTIES _________
    @property
    def kind(self) -> Constructs:
        return self._kind
    @kind.setter
    def kind(self, kind: str):
        try:
            self._kind = Constructs[kind]
        except:
            return ValueError(f"{kind} is not a supported Construct")

    # ENDPOINTS____________
    def add_endpoint(self, endpoint: EndpointNode.EndpointNode) -> None:
        """
        Adds an endpoint Node to the graph
        """
        self._endpoints[endpoint.name] = endpoint

    def remove_endpoint(self, name: str):
        """
        Removes an endpoint from the graph
        """
        self._endpoints.pop(name)
    
    def get_endpoint(self, name: str) -> EndpointNode.EndpointNode:
        """Retrieves an endpoint by name"""
        return self._endpoints[name]

        
    # RESOLVERS__________
    def add_resolver(self, resolver: ResolverNode.ResolverNode):
        """
        Add a resolver Node to the graph
        """
        self._resolvers[resolver.name] = resolver
    
    def remove_resolver(self, resolver_name: str):
        """Remove a resolver from the graph"""
        self._resolvers.pop(resolver_name)

    def get_resolver(self, name:str) -> ResolverNode.ResolverNode:
        if name not in self._resolvers:
            raise KeyError(f"Resolver {name} not registered in the system") 
        return self._resolvers[name]

    # PARAMETERS_________
    def add_parameter(self, param: ParamNode.ParamNode):
        """
        Add a parameter nod to the graph
        """
        self._params[param.name] = param

    def remove_parameter(self, param_name: str):
        """Remove parameter from graph"""
        self._params.pop(param_name)

    def get_param(self, name:str) -> ParamNode.ParamNode:
        try:
            return self._params[name]
        except:
            raise KeyError(f"{name} not a registered parameter")
    
    def __repr__(self) -> str:
        #TODO: Represent in tabular format
        return "Resolution Graph" 
    

    