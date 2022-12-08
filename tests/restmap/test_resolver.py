import pytest
from pathlib import Path
from restmap.resolver.nodes.resolvers import ResolverNode
from restmap.templateParser.TemplateParser import TemplateSchema
from restmap.manager.Manager import Manager
from restmap.resolver.Resolver import Resolver
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.resolver.nodes import EndpointNode, ParamNode
from restmap.templateParser.TemplateParser import TemplateParser

@pytest.fixture
def manager():
    return Manager(executor='AWS', name='TestStack')

@pytest.fixture
def template_path():
    return Path('./ingestless/tests/restmap/assets/complex_endpoint.yml')

@pytest.fixture
def template(manager:Manager, template_path: Path):
    return manager._parser.load(template_path)

# TESTS________________
class TestNodeResolution:

    def test__resolve_endpoint(self, 
        manager: Manager, 
        template_path: Path, 
        template:TemplateSchema, 
        ):
        manager.plan(template_path)
        endpoint = template.config.endpoints[0]
        name = list(endpoint.keys())[0]
        endpoint_dict = endpoint[name]
        response = manager._resolver._resolve_endpoint(name, endpoint_dict)
        assert isinstance(response, EndpointNode.EndpointNode)
        
    def test__resolve_resolvers(self, 
        manager: Manager, 
        template:TemplateSchema, 
        ):
        # TODO Must resolve EndpointResolvers to the Endpoint they are using (Get rid of the intermediary abstraction)
        # TODO Implement resolution of resolver without dependency to test it indipendently
        graph: ResolutionGraph = manager._resolver.resolve(template)
        resolver = list(template.config.resolvers.keys())[0]
        resolver_dict = template.config.resolvers[resolver]
        # response = manager._resolver._resolve_resolver(name='test', resolver=resolver_dict)
        # assert isinstance(response, EndpointNode.EndpointNode)
        # manager._resolver._resolve_resolver()
        assert False