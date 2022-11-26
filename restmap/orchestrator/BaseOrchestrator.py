"""

"""
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from restmap.compiler.function.FunctionCompiler import FunctionDeployment


@dataclass
class OrchestrationNode:
    """
    Represents an orchestrated construct and alows it to be 
    scheduled in an execution runtime 
    """
    parent: 'OrchestrationNode'
    children: List['OrchestrationNode']

@dataclass
class IteratorNode(OrchestrationNode):
    """
    Potential type to handle logic of iteration over a given range of 
    parameter inputs 
    
    Functionality:
    ---------------
    * Parametrize the relation between a function output and the input into another
    * 
    """
    parameter: dict

@dataclass
class Edge:
    """Stores attributes for the node"""
    params: dict = field(default_factory=dict)

    def set_params(self, params: dict):
        # Ensure only the defined parameters can be set
        self.params = params

@dataclass
class OrchestrationGraph:
    """
    Defines the orchestration graph that provides
    the management API to define the execution dependencies
    amongst the serverless constructs
    """
    nodes: List[OrchestrationNode] = field(default_factory=list)
    edges: Dict[Tuple,Edge] = field(default_factory=dict)
    adjs: Dict[int, set] = field(default_factory=dict)

    def insert(self, node: OrchestrationNode):
        """Adds a node to the graph"""
        # Keep track of nodes
        self.nodes.append(node)
        # Relate nodes
        self.adjs[len(self.nodes)] = set()
    
    def add_edge(self, node1: str, node2: str, params: dict={}):
        """Creates an edge between two nodes"""
        # Store attributes on the edge
        self.edges[(node1, node2), params] 
        # Insert Edge into graph
        self.adjs[self.nodes[node1]].add(node2)
        self.adjs[self.nodes[node2]].add(node1)

    def edge(self, node1:str, node2: str) -> Edge:
        assert all([node in self.nodes for node in [node1, node2]])
        try:
            return self.edges[(node1, node2)]
        except KeyError: 
            print("Relation between nodes {node1} and {node2} does not exist.")

    def update_edge(self, node1: str, node2: str, params: dict):
        """Updates values on the edge"""
        try:
            edge = self.edges[(node1, node2)]
            edge
        except KeyError:
            print("Relation between nodes {node1} and {node2} does not exist.")


class BaseOrchestrator:
    """
    The orchestrator schedules the execution of functions, 
    maintains their dependencies across runs and ensures
    that outputs from a function can be channeled to the 
    dependent functions to allow features such as parameter
    resolution from EndpointResolver without an intermediary
    storage system.

    What actually implements this interface is not defined, It can be a serverless system
    or a service. In case of a service, a REST integration or RPC interface would need to be implemented
    otherwise, the logic can be implemented against a given BackendProvider with its native services
    
    # TODO Can schedule a function to execute after another
    # TODO Can execute a function iteratively 
    # TODO Can pass the output of a function as input to the next
    # TODO Can retry a function if it fails

    """
    
    def __init__(self) -> None:
        self._functions = {str: FunctionDeployment}
        self.graph = OrchestrationGraph()

    def register(self, function: FunctionDeployment):
        """
        Register a function with the orchestrator 
        """
        self._functions[function.uid] = function


    def schedule(self, function: str):
        """
        Schedule a regular execution of a function
        @function: The UID of the function to be scheduled
        """
        try:
            function = self._functions[function]
        except KeyError:
            print(f"Function {function} is not registered in the system")
        raise NotImplementedError


    def schedule(self, function):
        raise NotImplementedError

    def schedule(self, function):
        raise NotImplementedError