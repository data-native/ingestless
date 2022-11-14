"""

"""
from typing import List
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
        self.resolvers: List[ResolverNode.ResolverNode] = []
        self.params: List[ParamNode.ParamNode] = []
        self.endpoints: List[EndpointNode.EndpointNode] = []

    # ENDPOINTS____________
    def add_endpoint(self, endpoint: EndpointNode.EndpointNode) -> None:
        """
        Adds an endpoint Node to the graph
        """
        self.endpoints.append(endpoint)

    def remove_endpoint(self, endpoint_name: str):
        """
        Removes an endpoint from the graph
        """
        self.endpoints = [ep for ep in self.endpoints if ep.name != endpoint_name ]
        
    # RESOLVERS__________
    def add_resolver(self, resolver: ResolverNode.ResolverNode):
        """
        Add a resolver Node to the graph
        """
        self.resolvers.append(resolver)
    
    def remove_resolver(self, resolver_name: str):
        """Remove a resolver from the graph"""
        self.resolvers = [rs for rs in self.resolvers if rs.name != resolver_name]
    
    # PARAMETERS_________
    def add_parameter(self, param: ParamNode.ParamNode):
        """
        Add a parameter nod to the graph
        """
        self.params.append(param)

    def remove_parameter(self, param_name: str):
        """Remove parameter from graph"""
        self.params = [par for par in self.params if par.name != param_name]
    
    def __repr__(self) -> str:
        #TODO: Represent in tabular format
        return "Resolution Graph" 
    

    