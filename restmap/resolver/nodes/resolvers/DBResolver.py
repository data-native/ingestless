"""

"""
from dataclasses import dataclass
from restmap.templateParser.TemplateParser import TemplateSchema
from .ResolverNode import ResolverNode

@dataclass
class _DBResolverBase:
    connectionstring: str
    table: str

@dataclass
class _DBResolverDefaults:
    pass

@dataclass
class DBResolver(_DBResolverDefaults, ResolverNode, _DBResolverBase):
    """
    Resolves data from a connection to a database.
    """
    
    def resolve(self, provider):
        pass
        