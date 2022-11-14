"""


"""
from restmap.templateParser.TemplateParser import TemplateSchema
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.resolver.nodes import EndpointNode, ParamNode, ResolverNode
class Resolver:
    """
    
    """

    def __init__(self) -> None:
        self.graph = ResolutionGraph()
    
    def resolve(self, template: TemplateSchema) -> ResolutionGraph:
        """
        Generate a resolved graph representation of the dependency
        parse tree. 

        The resolution creates:
        * An entry for each execution step
        * Looping contracts holding a compute step and associated attributes
        * Resolver nodes that when executed will read and provide a certain attribute
        """
        # Add all resolvers
        for resolver in template.config.resolvers:
            self.graph.add_resolver(resolver)

        # Add all parameters
        for param in template.config.params:
            self.graph.add_parameter(param)
        
        # Add all endpoints utilizing the resolver and parameter node references
        for endpoint in template.config.endpoints:
            self._resolve_endpoint(endpoint)
            self.graph.add_endpoint(endpoint)
    
    def _resolve_endpoint(self, endpoint) -> EndpointNode.EndpointNode:
        """
        Resolve the links mentioned in the resolutionTemplate
        """
        pass

    def _resolve_param(self, param: dict) -> ParamNode.ParamNode: 
        """
        Resolve the links mentioned in the resolutionTemplate
        """
        
        return ParamNode.ParamNode()

    def _resolve_resolver(self, resolver: dict) -> ResolverNode.ResolverNode:
        """
        Resolve the links mentioned in the resolutionTemplate
        """
        pass