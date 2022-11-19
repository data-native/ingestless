from pathlib import Path
import pytest
from restmap.templateParser.TemplateParser import TemplateSchema, TemplateParser
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.resolver.nodes import EndpointNode, ParamNode, BaseNode
from restmap.resolver.nodes.resolvers.ResolverNode import ResolverNode
from restmap.resolver.nodes.resolvers.EndpointResolver import EndpointResolver

@pytest.fixture()
def template_path():
    return Path('./ingestless/tests/restmap/assets/complex_endpoint.yml')

@pytest.fixture
def graph():
    return ResolutionGraph()

@pytest.fixture
def resolver(template_path: Path):
    parser = TemplateParser()
    template = parser.load(template_path)
    resolver_name = list(template.config.resolvers.keys())[0]
    resolver = EndpointResolver(
        name = resolver_name,
        **template.config.resolvers[resolver_name]
    )
    return resolver

@pytest.fixture
def param(resolver: ResolverNode):
    return ParamNode.ParamNode(
            name='scope',
            type='str',
            resolver= resolver
        )

@pytest.fixture
def endpoint(param: ParamNode.ParamNode):
    endpoint = EndpointNode.EndpointNode(
        kind='BaseEndpoint',
        descr='',
        name="",
        params=[param],
    )
    return endpoint

class TestEndpoints:

    def test_add_endpoint(self, graph: ResolutionGraph, endpoint: EndpointNode.EndpointNode):
        graph.add_endpoint(endpoint)
        assert len(graph._endpoints) == 1, "must add Endpoint to internal state"
        
    def test_remove_endpoint(self, graph: ResolutionGraph, endpoint: EndpointNode.EndpointNode):
        graph.add_endpoint(endpoint)
        response = graph.remove_endpoint(endpoint.name)
        assert len(graph._endpoints) == 0, "must remove EndpointNode from array of endpoints"

class TestParameters:

    def test_add_param(self, graph: ResolutionGraph, param: ParamNode.ParamNode):
        response = graph.add_parameter(param)
        assert len(graph._params) == 1, "must add ParamNode to array of parameters"

    def test_remove_param(self, graph: ResolutionGraph, param: ParamNode.ParamNode):
        graph.add_parameter(param) 
        response = graph.remove_parameter(param.name)
        assert len(graph._params) == 0, "must remove EndpointNode from array of endpoints"
    
class TestResolvers:

    def test_add_resolver(self, graph: ResolutionGraph, resolver: ResolverNode):
        response = graph.add_resolver(name=resolver.name, resolver=resolver)
        assert len(graph._resolvers) == 1, "must add ParamNode to array of parameters"
        assert graph._resolvers[resolver.name] == resolver

    def test_remove_resolver(self, graph: ResolutionGraph, resolver: ResolverNode):
        graph.add_resolver(name=resolver.name, resolver=resolver) 
        response = graph.remove_resolver(resolver.name)
        assert len(graph._resolvers) == 0, "must remove EndpointNode from array of endpoints"