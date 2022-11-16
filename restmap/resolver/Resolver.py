"""


"""
from restmap.resolver.nodes.resolvers import ResolverNode
from restmap.templateParser.TemplateParser import TemplateSchema
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.resolver.nodes import EndpointNode, ParamNode 
from restmap.resolver.nodes.resolvers import EndpointResolver, DBResolver
class Resolver:
    """
    The Resolver receives a TemplateSchema read from a yml configuration
    file and resolves all mentioned dependencies between the defined
    components. 

    This allows the user to flexibly define, reusable configuraton elements
    to manage complex, nested Rest API endpoint traversals. 

    Supported user stories
    -----------------
    * Can query an endpoint with a simple fully specified endpoint
    * Can query an endpoint with a varying url 

     
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
        #TODO: Ensure looping functionality can be compiled based on attributes and classes
        """
        # Add all resolvers
        for resolver in template.config.resolvers:
            resolver_template = template.config.resolvers[resolver]
            resolver_node = self._resolve_resolver(name=resolver, resolver=resolver_template)
            self.graph.add_resolver(resolver=resolver_node)

        # Add all parameters
        for param in template.config.params:
            param_template = template.config.params[param]
            param_node = self._resolve_param(param_template)
            self.graph.add_parameter(param=param_node)
        
        # Add all endpoints utilizing the resolver and parameter node references
        for endpoint in template.config.endpoints:
            for name, attributes in endpoint.items():
                endpoint_node = self._resolve_endpoint(name, attributes)
                self.graph.add_endpoint(endpoint_node)
        
        return self.graph
    
    def _resolve_endpoint(self, name: str,  endpoint: dict) -> EndpointNode.EndpointNode:
        """
        Resolve the links mentioned in the resolutionTemplate.
        """
        endpoint_switch = {
            'baseurl': EndpointNode.BaseURLNode,
            'relativeurl': EndpointNode.RelativeURLNode 
        }
        try:
            return self.graph._endpoints[name]
        except:
            endpoint['name'] = name
            # TODO: Ensure 'baseurl' are always resolved before 'relativeurl' endpoints. Parse SchemaTemplate into ordered_dict and sort accordingly before resolving
            if endpoint["kind"] == "relativeurl":
                endpoint['base'] = self.graph.get_endpoint(endpoint['base'])
            if "params" in endpoint:
                endpoint['params'] = [self.graph.get_param(name) for param in endpoint['params'] for name in param.keys()]
            return endpoint_switch[endpoint['kind']](**endpoint) 
        
    def _resolve_param(self, param: dict) -> ParamNode.ParamNode: 
        """
        Resolve the links mentioned in the resolutionTemplate
        Assumes prior resolution of resolvers.
        """
        try:
            # If already registered, return cached instance 
            return self.graph._params[param['name']]
        except:
            param['resolver'] = self.graph.get_resolver(param['resolver'])
            #TODO: Resolve authentication provider class (Enabling authentican configuration against provider backend)
            return ParamNode.ParamNode(**param)

    def _resolve_resolver(self, name: str, resolver: dict) -> ResolverNode.ResolverNode:
        """
        Resolve the links mentioned in the resolutionTemplate
        """
        # Resolver has no dependencies to resolve anymore
        resolver_switch = {
            'EndpointResolver': EndpointResolver.EndpointResolver,
            'DatabaseResolver': DBResolver.DBResolver
        }
        return resolver_switch[resolver['kind']](name=name, **resolver)