import pytest
from pathlib import Path
from restmap.resolver.nodes.resolvers import ResolverNode
from restmap.templateParser.TemplateParser import TemplateSchema
from restmap.manager.Manager import Manager
from restmap.resolver.Resolver import Resolver
from restmap.resolver.nodes import EndpointNode, ParamNode
from restmap.templateParser.TemplateParser import TemplateParser


@pytest.fixture
def resolver():
    return Resolver()

@pytest.fixture
def parser():
    return TemplateParser()

@pytest.fixture
def template_path():
    return Path('./tests/restmap/assets/templates/complex_endpoint.yml')

@pytest.fixture
def template(parser: TemplateParser, template_path: Path):
    return parser.load(template_path)

@pytest.fixture
def manager():
    return Manager()

# TESTS________________
class TestNodeResolution:

    def test__resolve_endpoint(self, 
        manager: Manager, 
        template_path: Path, 
        template:TemplateSchema, 
        resolver: Resolver
        ):
        manager.plan(template_path)
        endpoint = template.config.endpoints[0]
        response = resolver._resolve_endpoint(name=endpoint['name'], endpoint=endpoint)
        assert isinstance(response, EndpointNode.EndpointNode)
        
    def test__resolve_resolvers(self, 
        manager: Manager, 
        template_path: Path, 
        template:TemplateSchema, 
        resolver: Resolver
        ):
        manager.plan(template_path)
        resolver_dict = template.config.resolvers[0]
        response = resolver._resolve_resolver(resolver_dict)
        assert isinstance(response, EndpointNode.EndpointNode)