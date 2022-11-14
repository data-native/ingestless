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
        self.head = None
        self.resolvers: List[ResolverNode.ResolverNode] = []
        self.params: List[ParamNode.ParamNode] = []
        self.endpoints: List[EndpointNode.EndpointNode] = []
    
    def add_endpoint(self, endpoint: EndpointNode.EndpointNode) -> None:
        """
        Adds an endpoint Node to the graph
        """
        self.endpoints.append(endpoint)
    
    def add_resolver(self, resolver: ResolverNode.ResolverNode):
        """
        Add a resolver Node to the graph
        """
        self.resolvers.append(resolver)
        
    def add_parameter(self, param: ParamNode.ParamNode):
        """
        Add a parameter nod to the graph
        """
        self.params.append(param)

    
    def __repr__(self) -> str:
        #TODO: Represent in tabular format
        return "Resolution Graph" 
    

    