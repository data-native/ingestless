"""
Tests the Compiler Class that provides the 
public API of the Construction Compiler speciality classes.

Its API fronting needs to ensure that the Manager can successfully
request the compilation of templates for all supported Construct types
on the platform. 

Main Interaction
------------------
The compiler receives direct calls only from the Manager after
the `ResolutionGraph` was resolved by the Resolver service.

Main features to be ensured
---------------------------
* Compilation can happen for a template through its ResolutionGraph
* All entity types can be compiled from a parsed Template ResolutionGraph
* The compilation process can return informative messages on failing to create
  backend compilation target class instances due to misconfiguration, or validation errors
"""
import pytest
from restmap.templateParser.TemplateParser import TemplateParser
from restmap.resolver.Resolver import Resolver
from restmap.compiler.Compiler import Compiler

@pytest.fixture
def compiler():
  return Compiler()

def test_from_resolution_graph(compiler: Compiler):
  template = TemplateParser().load('./ingestless/tests/restmap/assets/complex_endpoint.yml')
  resolver = Resolver()
  resolutionGraph = resolver.resolve(template)
  compiler.from_resolution_graph(resolutionGraph)
  
  