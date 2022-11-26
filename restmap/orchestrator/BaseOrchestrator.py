"""

"""
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Union
from restmap.compiler.function.FunctionCompiler import FunctionDeployment


@dataclass
class OrchestrationNode:
    """
    Represents an orchestrated construct and alows it to be 
    scheduled in an execution runtime 
    """
    name: str
    parent: 'OrchestrationNode' = None
    children: List['OrchestrationNode'] = field(default_factory=list)

@dataclass
class IteratorNodeBase:
    parameter: dict
@dataclass
class IteratorNodeDefaults:
    pass
@dataclass
class IteratorNode(IteratorNodeDefaults, OrchestrationNode, IteratorNodeBase):
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
    #TODO Switch from reference by name to some internal UID to reduce memory footprint
    nodes: Dict[str, OrchestrationNode] = field(default_factory=dict)
    edges: Dict[Tuple,Edge] = field(default_factory=dict)
    adjs: Dict[str, set] = field(default_factory=dict)
    is_directed: bool = False

    def insert(self, node: Union[List[OrchestrationNode], OrchestrationNode]):
        """Adds a node or list of nodes to the graph"""
        if not isinstance(node, List):
            node = [node]
        # Keep track of nodes
        for el in node:
            self.nodes[el.name] = el
            # Relate nodes
            self.adjs[el.name] = set()

    def remove(self, node: str):
        """
        Removes a node from the graph, deleting all edges to and from
        it within the graph
        """
        if node not in self.nodes:
            return
        else:
            # Remove the relations in both directions
            for out_node in self.adjs[node]:
                self.remove_edge(node, out_node)
                # This fails silently when the edge doesn't exist
                self.remove_edge(out_node, node)
            del self.nodes[node]
            del self.adjs[node]
                
    def node(self, node: str) -> OrchestrationNode:
        """Retrieves the node from the graph for inspection"""
        try:
            return self.nodes[node]
        except KeyError:
            print(f"Node {node} not present in the graph")
    
    def add_edge(self, node1: str, node2: str, params: dict={}):
        """Creates an edge between two nodes"""
        # Store attributes on the edge
        self.edges[(node1, node2)] = params 
        # Insert Edge into graph
        self.adjs[node1].add(node2)
        if not self.is_directed:
            self.adjs[node2].add(node1)

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
            self.edges[(node1, node2)] = edge | params
        except KeyError:
            print("Relation between nodes {node1} and {node2} does not exist.")

    def remove_edge(self, node1: str, node2: str):
        """Removes an edge from the graph"""
        try:
            del self.edges[(node1, node2)]    
            if not self.is_directed:
                del self.edges[(node2, node1)]
        except KeyError:
            print(f"The edge between {node1} and {node2} does not exist, or the nodes are not registered")

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