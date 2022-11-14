"""

"""
from typing import Dict
from restmap.resolver.nodes import EndpointNode, ParamNode, ResolverNode, BaseNode

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
        self.head = None
        self.resolvers: Dict[str, ResolverNode.ResolverNode] = {}
        self.params: Dict[str, ParamNode.ParamNode] = {}
        self.endpoints: Dict[str, EndpointNode.EndpointNode] = {}

    # ENDPOINTS____________
    def add_endpoint(self, endpoint: EndpointNode.EndpointNode) -> None:
        """
        Adds an endpoint Node to the graph
        """
        self.endpoints[endpoint.name] = endpoint

    def remove_endpoint(self, endpoint_name: str):
        """
        Removes an endpoint from the graph
        """
        self.endpoints.pop(endpoint_name)
        
    # RESOLVERS__________
    def add_resolver(self, resolver: ResolverNode.ResolverNode):
        """
        Add a resolver Node to the graph
        """
        self.resolvers[resolver.name] = resolver
    
    def remove_resolver(self, resolver_name: str):
        """Remove a resolver from the graph"""
        self.resolvers.pop(resolver_name)
    
    # PARAMETERS_________
    def add_parameter(self, param: ParamNode.ParamNode):
        """
        Add a parameter nod to the graph
        """
        self.params[param.name] = param

    def remove_parameter(self, param_name: str):
        """Remove parameter from graph"""
        self.params.pop(param_name)
    
    def __repr__(self) -> str:
        #TODO: Represent in tabular format
        return "Resolution Graph" 
    

    