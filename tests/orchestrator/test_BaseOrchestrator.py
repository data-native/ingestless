"""
Test the orchestration graph implementation
that the provider specific Orchestration implementations
build upon. 
"""
import pytest
from pathlib import Path
from restmap.manager.Manager import Manager
from restmap.compiler.function.FunctionCompiler import FunctionDeployment, DeploymentParams
from restmap.orchestrator.BaseOrchestrator import BaseOrchestrator, OrchestrationGraph, OrchestrationNode

@pytest.fixture
def function():
    return  FunctionDeployment(
        code = '',
        code_location='', 
        runtime='python@3.10', 
        params=DeploymentParams(
        1, 1, 300, [], {}, [], True, True, 100
        ), 
        requirements=[]) 

@pytest.fixture
def orchestrator():
    return BaseOrchestrator()

@pytest.fixture
def graph():
    return OrchestrationGraph()

@pytest.fixture
def node():
    return OrchestrationNode('basenode', None)

@pytest.fixture
def manager():
    return Manager(name="TestStack", executor='AWS')

@pytest.fixture()
def template_path():
    return Path('./ingestless/tests/restmap/assets/complex_endpoint.yml')

class TestOrchestrator:
    """
    This tests the graph functionality underlying the orchestration 
    """
    #TODO Test difference in directional and undirectional graphs

    def test_can_init_orchestrator(self):
        orchestrator = BaseOrchestrator()
        assert isinstance(orchestrator.graph, OrchestrationGraph)
        assert isinstance(orchestrator._functions, dict)
        assert len(orchestrator._functions) == 1

class TestOrchestrationGraph:
    
    def test_can_init_graph(self, graph: OrchestrationGraph):
        dir_graph = OrchestrationGraph(is_directed=True)
        undir_graph = OrchestrationGraph(is_directed=False)
        assert dir_graph.is_directed == True
        assert undir_graph.is_directed == False
    
    def test_can_add_node(self,node: OrchestrationNode, graph: OrchestrationGraph):
        graph.insert(node)
        assert node.name in graph.nodes
        assert len(graph.nodes) == 1
        assert len(graph.adjs) == 1
        # Entering the same node twice will result in no addition
        graph.insert(node)
        assert len(graph.nodes) == 1
        assert len(graph.adjs) == 1
        node2 = OrchestrationNode(None, "secondnode")
        graph.insert(node2)
        assert len(graph.nodes) == 2, "Two individual nodes need to be created in the graph"
        assert len(graph.adjs) == 2, "Two entries need to be created in the adjecency list"
    
    def test_can_get_node(self, node: OrchestrationNode, graph: OrchestrationGraph):
        graph.insert(node)
        retrieved_node = graph.node(node.name)
        assert retrieved_node == node
    
    def test_can_remove_node(self, node: OrchestrationNode, graph: OrchestrationGraph):
        graph.insert(node)
        graph.remove(node.name)
        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0
        assert len(graph.adjs) == 0
    
    def test_can_add_edge(self, node: OrchestrationNode, graph: OrchestrationGraph):
        graph.insert(node)
        node2 = OrchestrationNode(None, "secondnode")
        graph.insert(node2)
        graph.add_edge(node.name, node2.name)
        assert len(graph.adjs[node.name]) == 1, "An adjacency entry must be added for node"
        if graph.is_directed:
            assert len(graph.adjs[node2.name]) == 0, "In a directed graph the inverse relation is still unset"
        else: 
            assert len(graph.adjs[node2.name]) == 1, "In a undirected graph but relations are added"

    def test_can_remove_edge(self, node: OrchestrationNode, graph: OrchestrationGraph):
        node2 = OrchestrationNode(None, "secondnode")
        graph.insert([node, node2])
        graph.add_edge(node.name, node2.name)
        graph.remove_edge(node.name, node2.name)


    def test_can_update_edge(self, node: OrchestrationNode, graph: OrchestrationGraph):
        node2 = OrchestrationNode(None, "secondnode")
        graph.insert([node, node2])
        graph.add_edge(node.name, node2.name)
        update_dict = {
                'status': 'updated'
                }
        graph.update_edge(node.name, node2.name, update_dict)
        assert graph.edges[(node.name, node2.name)] == update_dict, "Updates to an initial edge params should contain all elements of the update only"
        param_addition_dict = {
                'PreviousState': 'unset'}
        graph.update_edge(node.name, node2.name, param_addition_dict)
        assert graph.edges[(node.name, node2.name)] == update_dict | param_addition_dict, "Updates to an existing parametrization contain the union of the dicts. Whereby the new updates overwrite existing params"

class TestOrchestrator:
    """
    Tests the functionality around data graph creation, parsing, traversal 
    and integration with the chosen BackendProvider
    """

    def test_register(self, function: FunctionDeployment, orchestrator: BaseOrchestrator):
        orchestrator.register(function)
        assert orchestrator._functions[function.uid] == function, "DeployableConstruct instnace must be stored in the orchestrator by uid reference"
        assert function.uid in orchestrator.graph.nodes, "Orchestration Node for the DeployableConstruct must be created in the graph"

    # must be able to schedule a function with a cron definition
    def test_schedule(self, function: FunctionDeployment, orchestrator: BaseOrchestrator):
        pass

    def test_trigger(self, function: FunctionDeployment, orchestrator: BaseOrchestrator):
        """Sets a dependency between two function"""
        from copy import deepcopy
        func2 = deepcopy(function)
        func2.uid = "SomethingElse"
        orchestrator.register(function)
        orchestrator.register(func2)
        orchestrator.add_trigger(function.uid, 'success', func2.uid)
        assert orchestrator.graph.edges[(function.uid, func2.uid)]

    def test_orchestrate(self, template_path: Path, manager: Manager):
        """
        The orchestration function depends on a complex preparation of objects
        and should be tested with mock objects instead.

        #TODO Move 
        """
        template = manager._parser.load(template_path)
        resolution_graph = manager._resolver.resolve(template)
        orchestration_graph = manager._orchestrator.orchestrate(resolution_graph)
        assert isinstance(orchestration_graph, OrchestrationGraph)

class TestOrchestrationNode:
    """
    Tests the dependency attribution API on the 
    OrchestrationNode class that is used within the 
    framework to specify inter function dependencies.
    """
    pass
        # Create the dependencies


        

    # must be able to load data from CompilerGraph
    # must be able to schedule a function on a given scheduled trigger
    # must be able to schedule a function success run triggering another function

