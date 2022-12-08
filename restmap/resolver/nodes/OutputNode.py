
from dataclasses import dataclass
from restmap.templateParser.TemplateParser import TemplateSchema
from restmap.resolver.nodes.BaseNode import BaseNode

@dataclass
class _OutputNodeBase:
    kind: str
    provider: dict
@dataclass
class _OutputNodeDefaults:
    authentication: dict = None
@dataclass
class OutputNode(_OutputNodeDefaults, BaseNode, _OutputNodeBase):
    """
    A resolver that provides an single or iterable
    value for a given parameter value in other services.
    """
    pass     

@dataclass
class _BlobOutputNodeBase:
    pass
@dataclass
class _BlobOutputNodeDefaults:
    pass
@dataclass
class BlobOutputNode(_BlobOutputNodeDefaults, OutputNode, _BlobOutputNodeBase):
    pass

@dataclass
class TableOutputNode(OutputNode):
    pass

@dataclass
class QueueOutputNode(OutputNode):
    pass

@dataclass
class DatabaseOutputNode(OutputNode):
    pass