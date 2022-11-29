from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, Union

from restmap.compiler.function.FunctionCompiler import FunctionDeployment

@dataclass
class OrchestrationNode:
    """
    Represents an orchestrated construct and alows it to be 
    scheduled in an execution runtime 
    """
    name: str
    construct: FunctionDeployment
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
class EdgeParams:
    """
    @triggers: Resolution of base triggers target node
    @on: List of outcome types to execute defined trigger for
    """
    triggers : bool
    on: List[str]


@dataclass
class Edge:
    """Stores attributes for the node"""
    params: EdgeParams 

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
