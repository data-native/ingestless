"""

"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Union
from restmap.compiler.function.FunctionCompiler import FunctionDeployment
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.executor.BaseExecutor import BaseExecutor


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

class BaseOrchestrator(ABC):
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
    
    def __init__(self, executor: BaseExecutor) -> None:
        self._functions = {str: FunctionDeployment}
        self.graph = OrchestrationGraph(is_directed=True)
        self.executor = executor


    # PUBLIC API_______________
    def orchestrate(self, deployables: List[FunctionDeployment], resolution_graph: ResolutionGraph) -> OrchestrationGraph:
        """
        Resolves the dependencies between the deployables and 
        computes an execution graph that can be executed by any 
        Executor instance against the chosen backend.
        """
        from restmap.resolver.nodes. EndpointNode import RelativeURLNode
        # TODO Place all executable functions on the graph
        orch_nodes = [OrchestrationNode(
            construct=deployable, 
            name=deployable.uid,
            ) for deployable in deployables]
        self.graph.insert(orch_nodes)
        # TODO Create edges between nodes if they are dependent
        # TODO Find a way to generalize this logic to handle various template types
        for name, resolver in resolution_graph._resolvers.items():
           # Have to handle each nodes resolution indipendently based on its inherent logic. TODO Find a way to generalize this
            if resolver.kind == "EndpointResolver":
               # Set this to ('depends_on')
               self.graph.add_edge(resolver.endpoint.name, name)
        
        # Manages nested dependencies amongst endpoints
        for name, endpoint in resolution_graph._endpoints.items():
            if not isinstance(endpoint, RelativeURLNode):
                continue
            self.graph.add_edge(endpoint.base.name, name)
            # Sets a dependency on all resolvers resolving the parameters used in the endpoint
            for param in endpoint.params:
                # TODO Potentially add parametrization on the edge to enable iteration over parameter space
                self.graph.add_edge(param.resolver.name, name)

        return self.graph

    # Mainly internal methods_____________
    def register(self, function: FunctionDeployment):
        """
        Register a function with the orchestrator 
        """
        self._functions[function.uid] = function
        node =  OrchestrationNode(
                name=function.uid,
                construct = function
                )
        self.graph.insert(node)

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


    def add_trigger(self, function: str, on:Union[str, List[str]], triggered: str):
        """
        Configures a trigger on event between two functions

        @function: the function acting as the trigger
        @on: The type(s) of events to schedule the trigger on
        @triggered: The function to be triggered
        """
        if isinstance(on, str):
            on = [on]
        # TODO Set the type of trigger on the edge
        self.graph.add_edge(function, triggered, EdgeParams(
            triggers=True,
            on=on
            ))

    def subgraphs(self):
        """
        Returns the set of disconnected graphs acting as 
        individual, unrelated units of deployment.
        """
        subgraphs = []
        nodes_without_incoming_edges = {edge[1] for edge in self.graph.edges}
        independent_nodes = set(self.graph.nodes.keys()).difference(nodes_without_incoming_edges)

        # ubgraph, export as individual OrchestrationGraph instance
        for node in independent_nodes:
            # TODO Extend this to follow all edges in the subgraph
            subgraph_edges = {k:v for k,v in self.graph.edges.items() if k[0] == node} 
            while True:
                # Append all edges for the edge targets
                next_degree_nodes = {k:v for k,v in self.graph.edges.items() for child in subgraph_edges.keys() if k[0] in child[1]}
                # Recurses over all levels of connection in the graph until it finds no more edges to add
                if not set(next_degree_nodes.keys()).difference(set(subgraph_edges.keys())):
                    break
                subgraph_edges = subgraph_edges | next_degree_nodes

            # Compute the set of nodes to include in the subgraph
            subgraph_node_keys = {node for tup in subgraph_edges for node in tup}
            subgraph_nodes = {k:v for k,v in self.graph.nodes.items() if k in subgraph_node_keys}
            subgraph = OrchestrationGraph(
                adjs={node: self.graph.adjs[node]}, 
                edges=subgraph_edges,
                nodes=subgraph_nodes,
                )
            yield subgraph
    
    def deploy(self, graph: OrchestrationGraph, dryrun: bool=False):
        """
        Deploy the orchestrated graph onto the selected backend.

        @dryrun: Compiles the IaC backend state, but does not deploy the configuration
        """
        self._deploy_to_executor(graph)

    @abstractmethod
    def _deploy_to_executor(self, graph: OrchestrationGraph):
        """
        Implements the logic to deploy the common strucure of the 
        orchestration graph onto the specific executor.
        The business logic of the implementation in this function
        and all supporting subfunctions contain the specific approach
        of the given orchestrator plug-in.

        All functional code used for the actual IaC compilation must be 
        implemented in the associated Executor
        """
        raise NotImplementedError