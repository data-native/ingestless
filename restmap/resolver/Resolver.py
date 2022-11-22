"""


"""
from typing import Dict, List 
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

    def resolve(self, template: TemplateSchema):
        """
        Generate a tree of nodes that can be resolved one after
        the other to reach a full resolution of all dependencies
        defined in the template. 

        """
        # TODO Find a way to identify circular dependencies that can't be resolved and fail 
        self.graph.kind = template.kind 
        # Starts from the full list of unresolved elements and removes them until all have been resolved
        # Each section ['endpoint', 'param', 'resolver'] checks that it still exists as it is removed on full resolution of all its items
        unresolved: Dict[str, List[str]] = {
            'endpoint': [name for endpoint in template.config.endpoints for name in endpoint.keys()] ,
            'param': [param for param in template.config.params.keys()],
            'resolver': [resolver for resolver in template.config.resolvers.keys()],
        }
        # Iterates until all dependencies where met
        repetition = 0
        max_repetition = 20 # TODO Remove this hardcoded max_iteration with a smart circular dependency check
        while unresolved['endpoint'] and unresolved['param'] and unresolved['resolver']: 
            repetition += 1        
            if repetition == max_repetition:
                raise ValueError("You have created a circular dependency the system can't resolve. Please check your dependencies.")
            # Try to start with the elements least likely to have dependencies
            if 'resolver' in unresolved:
                for name, attributes in template.config.resolvers.items():
                    try:
                        if not 'resolver' in unresolved or name not in unresolved['resolver']:
                            pass
                        elif attributes['kind'] == 'EndpointResolver' and attributes['endpoint'] in unresolved['endpoint']:
                            pass
                        else:
                            self.graph.add_resolver(self._resolve_resolver(name, attributes))
                            unresolved['resolver'] = [r for r in unresolved['resolver'] if r != name]
                    except KeyError:
                        pass
            if 'param' in unresolved:
                for param in template.config.params:
                    param_template = template.config.params[param]
                    if 'param' in unresolved and param not in unresolved['param']:
                        pass
                    elif 'resolver' in param_template and 'resolver' in unresolved and  param_template['resolver'] in unresolved['resolver']:
                        # Depends on unresolved resolver must try again
                        pass
                    else:
                        self.graph.add_parameter(self._resolve_param(param_template)) 
                        if 'param' in unresolved:
                            unresolved['param'] = [p for p in unresolved['param'] if p != param]
            if 'endpoint' in unresolved:
                for endpoint in template.config.endpoints:
                    for name, attributes in endpoint.items():
                        if name not in unresolved['endpoint']:
                            pass
                        # Handle the case with a relative endpoint
                        elif attributes['kind'] == "relativeurl" and attributes['base'] in unresolved['endpoint']:
                            pass
                        elif 'params' in attributes and any([name in unresolved['param'] for param in attributes['params'] for name in param.keys()]):
                            # Not yet fully resolved
                            pass
                        else:
                            self.graph.add_endpoint(self._resolve_endpoint(name, attributes))
                            unresolved['endpoint'] = [e for e in unresolved['endpoint'] if e != name]
        return self.graph 

    # TODO This must be rewritten to actually compile a full resolution of all attributes
    def _old_resolve(self, template: TemplateSchema) -> ResolutionGraph:
        """
        Generate a resolved graph representation of the dependency
        parse tree.

        The resolution creates:
        * An entry for each execution step
        * Looping contracts holding a compute step and associated attributes
        * Resolver nodes that when executed will read and provide a certain attribute
        #TODO: Ensure looping functionality can be compiled based on attributes and classes
        """

        self.graph.kind = template.kind
        # Add all resolvers
        for resolver in template.config.resolvers:
            resolver_template = template.config.resolvers[resolver]
            if resolver_template['kind'] == 'EndpointResolver':
                resolver_template['endpoint'] = template.config.endpoints[resolver]
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
        if resolver['kind'] == 'EndpointResolver':
            resolver['endpoint'] = self.graph._endpoints[resolver['endpoint']]
        return resolver_switch[resolver['kind']](name=name, **resolver)