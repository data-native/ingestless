"""
Endpoint nodes define the execution parameters to integrate 
with a chosen API endpoint. All other components in the framework
serve the configuration of these nodes in the Resolution Graph. 

Each node has both required and optional parameters that are defined
in composable parent classes to retain the correct ordering of default
parameters in the autogenerated __init__ definition. 

Nodes
----------------
EndpointNode: Defines overall Endpoint node attributes and behavior
BaseURLNode: Carries reusable parameters to configure a base URL to integrate
RelativeURLNode: Builds up on the BaseURLNode endpoint configuration to execute
                 integration with a specific relative URL. It generates the
                 resolution against the BackendProvider to parametrize the execution
                 function.

"""
from dataclasses import dataclass, field
from .BaseNode import BaseNode
from restmap.resolver.nodes.ParamNode import ParamNode

@dataclass
class _EndpointNodeBase:
    kind: str
@dataclass
class _EndpointNodeDefaults:
    params: list[ParamNode] = field(default_factory=list)
@dataclass
class EndpointNode(_EndpointNodeDefaults, BaseNode, _EndpointNodeBase):
    """
    Represents a logical REST endpoint in the computation
    graph. Parametrization on this node can either be hardcoded, 
    or provided through a resolver instance.
    """

    def resolve(self, provider):
        raise NotImplementedError
    
    
    @property
    def format_params(self) -> dict[str, str]:
        """
        Returns the list of params for parametrization of a format string
        return: dictionary mapping of param name to param value
        """
        raise NotImplementedError
    

@dataclass 
class _BaseURLNodeBase:
    url: str
@dataclass 
class _BaseURLNodeDefaults:
    pass
@dataclass
class BaseURLNode(_BaseURLNodeDefaults, EndpointNode, _BaseURLNodeBase):
    """
    A configuration url base endpoint that is not executed by itself
    but carries configuration that is reused across RelativeURLNodes.
    """
    def get_url(self):
        raise NotImplementedError
        # return self.url.format(**self.params)

@dataclass 
class _RelativeURLNodeBase:
    base: BaseURLNode
    relative: str 
@dataclass 
class _RelativeURLNodeDefaults:
    pass
@dataclass
class RelativeURLNode(_RelativeURLNodeDefaults, EndpointNode, _RelativeURLNodeBase):
    """
    A configuration url base endpoint that is not executed by itself
    but carries configuration that is reused across RelativeURLNodes.
    """
    def get_url(self):
        return self.base.get_url() + self.relative.format(**self.format_params)