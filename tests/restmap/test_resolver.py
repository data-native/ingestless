import pytest
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.resolver.nodes import EndpointNode, ParamNode, ResolverNode, BaseNode


@pytest.fixture
def graph():
    return ResolutionGraph()

@pytest.fixture
def resolver():
    resolver = ResolverNode.ResolverNode(
        name="db_scope_resolver"
    )
    return resolver

@pytest.fixture
def param(resolver: ResolverNode.ResolverNode):
    return ParamNode.ParamNode(
            name='scope',
            type='str',
            resolver= resolver
        )

@pytest.fixture
def endpoint(param: ParamNode.ParamNode):
    endpoint_dict = {
        'name': 'google_maps_api',
        'base_url': 'https://www.google.com/',
        'params': [param]
    }
    endpoint = EndpointNode.EndpointNode(**endpoint_dict)
    return endpoint

class TestEndpointResolver:

    def test_add_endpoint(self, graph: ResolutionGraph, endpoint: EndpointNode.EndpointNode):
        response = graph.add_endpoint(endpoint)
        assert len(graph.endpoints) == 1, "must add EndpointNode to array of endpoints"
        assert graph.endpoints[0] == endpoint, "first entry in endpoints must be endpoint instance"

    def test_remove_endpoint(self, graph: ResolutionGraph, endpoint: EndpointNode.EndpointNode):
        graph.add_endpoint(endpoint) 
        response = graph.remove_endpoint(endpoint.name)
        assert len(graph.endpoints) == 0, "must remove EndpointNode from array of endpoints"

class TestParameterResolver:

    def test_add_param(self, graph: ResolutionGraph, param: ParamNode.ParamNode):
        response = graph.add_parameter(param)
        assert len(graph.params) == 1, "must add ParamNode to array of parameters"
        assert graph.params[0] == param, "first entry in params must be param instance"

    def test_remove_param(self, graph: ResolutionGraph, param: ParamNode.ParamNode):
        graph.add_parameter(param) 
        response = graph.remove_parameter(param.name)
        assert len(graph.params) == 0, "must remove EndpointNode from array of endpoints"

class TestResolver:

    def test_add_resolver(self, graph: ResolutionGraph, resolver: ResolverNode.ResolverNode):
        response = graph.add_resolver(resolver)
        assert len(graph.resolvers) == 1, "must add ParamNode to array of parameters"
        assert graph.resolvers[0] == resolver, "first entry in params must be param instance"

    def test_remove_resolver(self, graph: ResolutionGraph, resolver: ResolverNode.ResolverNode):
        graph.add_resolver(resolver) 
        response = graph.remove_resolver(resolver.name)
        assert len(graph.resolvers) == 0, "must remove EndpointNode from array of endpoints"