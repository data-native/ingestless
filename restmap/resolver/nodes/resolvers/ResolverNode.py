from dataclasses import dataclass
from restmap.templateParser.TemplateParser import TemplateSchema
from restmap.resolver.nodes.BaseNode import BaseNode

@dataclass
class _ResolverNodeBase:
    kind: str
    authentication: dict

@dataclass
class _ResolverNodeDefaults:
    pass

@dataclass
class ResolverNode(_ResolverNodeDefaults, BaseNode, _ResolverNodeBase):
    """
    A resolver that provides an single or iterable
    value for a given parameter value in other services.
    """
    def authenticate(self):
        """
        Authenticates to the target service
        """
        raise NotImplementedError
    
    def resolve(self):
        """
        Resolves the parameter from the associated 
        """
         