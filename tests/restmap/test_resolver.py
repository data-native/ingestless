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
