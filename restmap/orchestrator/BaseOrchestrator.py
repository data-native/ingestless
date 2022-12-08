"""

"""
from abc import ABC, abstractmethod
from typing import List, Union, Any

from restmap.compiler.function.FunctionCompiler import FunctionDeployment
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.resolver.nodes.EndpointNode import BaseURLNode 
from restmap.executor.AbstractBaseExecutor import AbstractBaseExecutor
from .OrchestrationGraph import OrchestrationGraph, OrchestrationNode, EdgeParams
from restmap.compiler.BaseCompiler import BaseCompiler

class AbstractOrchestrator(ABC):
    pass

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
    
    def __init__(self, 
        executor: AbstractBaseExecutor,
        compiler: BaseCompiler
        )-> None:
        self._functions = {str: FunctionDeployment}
        self.graph = OrchestrationGraph(is_directed=True)
        self.executor = executor
        self.compiler = compiler

    # PUBLIC API_______________
    def orchestrate(self, resolution_graph: ResolutionGraph) -> OrchestrationGraph:
        """
        Resolves the dependencies between the deployables and 
        computes an execution graph that can be executed by any 
        Executor instance against the chosen backend.
        """
        from restmap.resolver.nodes.EndpointNode import RelativeURLNode

        # TODO Place all executable functions on the graph
        # TODO Manage list of executables in the template schema in a single source of truth configuration. Currently this info is duplicated in the framework
        # Only Relative URL Endpoints are executables
        orch_nodes = [OrchestrationNode(
            construct=endpoint, 
            name=name
            ) for name, endpoint in resolution_graph._endpoints.items() if not isinstance(endpoint, BaseURLNode)]
        
        # All resolvers are executables
        orch_nodes.extend([OrchestrationNode(
            construct=resolver, 
            name=name
            ) for name, resolver in resolution_graph._resolvers.items()])
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
            if isinstance(endpoint, RelativeURLNode):
                # self.graph.add_edge(endpoint., name)
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

    def subgraphs(
        self,
        graph: OrchestrationGraph
        ):
        """
        Returns the set of disconnected graphs acting as 
        individual, unrelated units of deployment.
        """
        nodes_without_incoming_edges = {edge[1] for edge in graph.edges}
        independent_nodes = set(graph.nodes.keys()).difference(nodes_without_incoming_edges)

        # ubgraph, export as individual OrchestrationGraph instance
        for node in independent_nodes:
            # TODO Extend this to follow all edges in the subgraph
            subgraph_edges = {k:v for k,v in graph.edges.items() if k[0] == node} 
            while True:
                # Append all edges for the edge targets
                next_degree_nodes = {k:v for k,v in graph.edges.items() for child in subgraph_edges.keys() if k[0] in child[1]}
                # Recurses over all levels of connection in the graph until it finds no more edges to add
                if not set(next_degree_nodes.keys()).difference(set(subgraph_edges.keys())):
                    break
                subgraph_edges = subgraph_edges | next_degree_nodes

            # Compute the set of nodes to include in the subgraph
            subgraph_node_keys = {node for tup in subgraph_edges for node in tup}
            subgraph_nodes = {k:v for k,v in graph.nodes.items() if k in subgraph_node_keys}
            subgraph = OrchestrationGraph(
                adjs={node: graph.adjs[node]}, 
                edges=subgraph_edges,
                nodes=subgraph_nodes,
                )
            yield subgraph
    
    def deploy(self, deployables: List[FunctionDeployment], graph: OrchestrationGraph, dryrun: bool=False):
        """
        Deploy the orchestrated graph onto the selected backend.

        @dryrun: Compiles the IaC backend state, but does not deploy the configuration
        """
        # Attach the graph nodes to their deployables as constructs
        graph.nodes = {
            name: { 
                'deployment': deployables[name], 
                'node': node}
            for name,node in graph.nodes.items()}
        self._deploy_to_executor(graph)

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

# Interface Registration
AbstractBaseExecutor.register(BaseOrchestrator)