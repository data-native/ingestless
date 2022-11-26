"""
Test the orchestration graph implementation
that the provider specific Orchestration implementations
build upon. 
"""
import pytest
from restmap.orchestrator.BaseOrchestrator import BaseOrchestrator, OrchestrationGraph, OrchestrationNode

@pytest.fixture
def orchestrator():
    return BaseOrchestrator()

@pytest.fixture
def graph():
    return OrchestrationGraph()

class TestOrchestrator:
    """
    This tests the graph functionality underlying the orchestration 
    """

    def test_can_init_orchestrator(self):
        orchestrator = BaseOrchestrator()
        assert isinstance(orchestrator.graph, OrchestrationGraph)
        assert isinstance(orchestrator._functions, dict)
        assert len(orchestrator._functions) == 1
    

class TestOrchestrationGraph:
    
    def test_can_init_graph(self, graph: OrchestrationGraph):
        assert graph.edges
        assert graph.nodes
        assert graph.adjs
    
    def test_can_add_node(self, graph: OrchestrationGraph):
        node = OrchestrationNode(None, [])
        graph.insert(node)
        assert node in graph.nodes
        assert len(graph.nodes) == 1
        assert len(graph.adjs) == 1
        graph.insert(node)
        assert len(graph.nodes) == 2
        assert len(graph.adjs) == 2
    
    def 
        
        

