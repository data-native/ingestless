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
from restmap.resolver.Resolver import Resolver, ResolutionGraph
from restmap.compiler.Compiler import Compiler
from restmap.compiler.function.FunctionCompiler import DeployableFunction

@pytest.fixture
def compiler():
  return Compiler()

@pytest.fixture
def template():
  return TemplateParser().load('./ingestless/tests/restmap/assets/complex_endpoint.yml')

@pytest.fixture
def res_graph(template):
  resolver = Resolver()
  return resolver.resolve(template)

def test_from_resolution_graph(compiler: Compiler, res_graph: ResolutionGraph):
  deployment = compiler.from_resolution_graph(res_graph)
  assert all([isinstance(d, DeployableFunction) for d in deployment ]), "Compilation should return a list of DeployableComponent instances"
  
#TODO Extend the tests
def test_compile_endpoint(compiler: Compiler, res_graph: ResolutionGraph):
  deployment = compiler.from_resolution_graph(res_graph)
  
  
  