from dataclasses import dataclass
from restmap.resolver.nodes.BaseNode import BaseNode
from restmap.resolver.nodes.resolvers import ResolverNode

@dataclass
class _ParamNodeBase:
    type: str
    resolver: ResolverNode.ResolverNode

@dataclass
class _ParamNodeDefaultsBase:
    pass

@dataclass
class ParamNode(_ParamNodeDefaultsBase, BaseNode, _ParamNodeBase):
    """
    
    """
    def resolve(self, provider):
        """
        Returns the value of the parameter
        """
        return self.resolver.resolve()
        