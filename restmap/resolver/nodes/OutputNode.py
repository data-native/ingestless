
from dataclasses import dataclass
from restmap.templateParser.TemplateParser import TemplateSchema
from restmap.resolver.nodes.BaseNode import BaseNode

@dataclass
class _OutputNodeBase:
    kind: str
    authentication: dict

@dataclass
class _OutputNodeDefaults:
    pass

@dataclass
class OutputNode(_OutputNodeDefaults, BaseNode, _OutputNodeBase):
    """
    A resolver that provides an single or iterable
    value for a given parameter value in other services.
    """
    pass     