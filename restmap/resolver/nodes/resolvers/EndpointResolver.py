from dataclasses import dataclass
from restmap.templateParser.TemplateParser import TemplateSchema
from .ResolverNode import ResolverNode
from ..EndpointNode import EndpointNode

@dataclass
class _EndpointResolverBase:
    endpoint: EndpointNode

@dataclass
class _EndpointResolverDefault:
    pass

@dataclass
class EndpointResolver(_EndpointResolverDefault, ResolverNode, _EndpointResolverBase):
    """
    Resolves attributes from a url endpoint
    dynamically and provides the resolved 
    value to the attributed functions.
    """

    def resolve(self, provider):
        """
        Resolve functionality provides the resolved
        value back to the caller to iteratively resolve
        the value.
        """
        return self.endpoint.resolve(provider)
    
    def authenticate(self):
        pass

