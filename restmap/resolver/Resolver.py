"""


"""
from typing import Dict, List 
from restmap.resolver.nodes.resolvers import ResolverNode
from restmap.templateParser.TemplateParser import TemplateSchema
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.resolver.nodes import EndpointNode, ParamNode, OutputNode
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
            'output': [output for output in template.config.outputs.keys()]
        }
        # TODO Check if this can be futher optimized 
        num_unresolved_prev = 0 
        num_curr_unresolved = sum([len(list(l)) for l in unresolved.values()])
        # Iterates until all dependencies where met
        while unresolved['endpoint'] or unresolved['param'] or unresolved['resolver'] or unresolved['output']: 
            num_curr_unresolved = sum([len(list(l)) for l in unresolved.values()])
            # if num_unresolved_prev > 0:
                # if num_unresolved_prev == num_curr_unresolved:
                    # raise ValueError("You have created a circular dependency the system can't resolve. Please check your dependencies.")
            num_unresolved_prev = num_curr_unresolved
            
            # Try to start with the elements least likely to have dependencies
            if len(unresolved['output']):
                for name, attributes in template.config.outputs.items():
                    try:
                        if not 'output' in unresolved or name not in unresolved['output']:
                            pass
                        else:
                            self.graph.add('output', self._resolve_output(name, attributes))
                            unresolved['output'] = [o for o in unresolved['output'] if o != name]
                    except KeyError:
                        pass
            if len(unresolved['resolver']):
                for name, attributes in template.config.resolvers.items():
                    try:
                        if name not in unresolved['resolver']:
                            pass
                        elif attributes['kind'] == 'EndpointResolver' and attributes['endpoint'] in unresolved['endpoint']:
                            pass
                        else:
                            self.graph.add('resolver', self._resolve_resolver(name, attributes))
                            unresolved['resolver'] = [r for r in unresolved['resolver'] if r != name]
                    except KeyError:
                        pass
            if len(unresolved['param']):
                for param in template.config.params:
                    param_template = template.config.params[param]
                    if param not in unresolved['param']:
                        pass
                    elif 'resolver' in param_template and 'resolver' in unresolved and  param_template['resolver'] in unresolved['resolver']:
                        # Depends on unresolved resolver must try again
                        pass
                    else:
                        self.graph.add('param', self._resolve_param(param_template)) 
                        if 'param' in unresolved:
                            unresolved['param'] = [p for p in unresolved['param'] if p != param]
            if len(unresolved['endpoint']):
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
                            self.graph.add('endpoint', self._resolve_endpoint(name, attributes))
                            unresolved['endpoint'] = [e for e in unresolved['endpoint'] if e != name]
        return self.graph 

    # TODO This must be rewritten to actually compile a full resolution of all attributes
    def _resolve_endpoint(self, name: str,  endpoint: dict) -> EndpointNode.EndpointNode:
        """
        Resolve the links mentioned in the resolutionTemplate.
        """
        endpoint_switch = {
            'baseurl': EndpointNode.BaseURLNode,
            'relativeurl': EndpointNode.RelativeURLNode 
        }
        try:
            return self.graph.get('endpoint', name)
        except:
            endpoint['name'] = name
            # TODO: Ensure 'baseurl' are always resolved before 'relativeurl' endpoints. Parse SchemaTemplate into ordered_dict and sort accordingly before resolving
            if endpoint["kind"] == "relativeurl":
                endpoint['base'] = self.graph.get('endpoint', endpoint['base'])
            if "params" in endpoint:
                endpoint['params'] = [self.graph.get('param', name) for param in endpoint['params'] for name in param.keys()]
            return endpoint_switch[endpoint['kind']](**endpoint) 
        
    def _resolve_param(self, param: dict) -> ParamNode.ParamNode: 
        """
        Resolve the links mentioned in the resolutionTemplate
        Assumes prior resolution of resolvers.
        """
        try:
            # If already registered, return cached instance 
            return self.graph.get('param', param['name'])
        except:
            param['resolver'] = self.graph.get('resolver', param['resolver'])
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
            resolver['endpoint'] = self.graph.get('endpoint', resolver['endpoint'])
        return resolver_switch[resolver['kind']](name=name, **resolver)

    def _resolve_output(self, name: str, output: dict) -> OutputNode.OutputNode:
        """
        Resolve the output links defined on the endpoints
        """
        output_switch = {
            'blob': OutputNode.BlobOutputNode,
            'table': OutputNode.TableOutputNode,
            'queue': OutputNode.QueueOutputNode,
            'database': OutputNode.DatabaseOutputNode    
        }
        try: 
            return self.graph.get('output', name)
        except:
            output['name'] = name
            return output_switch[output['kind']](**output) 