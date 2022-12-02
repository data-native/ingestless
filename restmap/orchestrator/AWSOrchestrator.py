"""
Implmements an AWS native Orchestrator

Services used:
--------------
* EventGrid Scheduler
"""
from restmap.executor.AbstractBaseExecutor import AbstractBaseExecutor
from .BaseOrchestrator import BaseOrchestrator, OrchestrationGraph


class EventGridOrchestrator(BaseOrchestrator):
    """
    AWS native serverless orchestrator implementation that
    focusses on fully serverless design without continuously running
    manager service (headless).

    Builds on the AWS EventGrid Scheduler service, native serverless
    trigger configuration and event queues for data passing amongst the 
    functions. 
    """
    
    def __init__(self, executor: AbstractBaseExecutor):
        super().__init__(executor)

    # EXECUTOR INTERACTION____________
    # Intended to separate the basic orchestration logic in the BaseOrchestrator
    # from the changing logic implemented by a specific stack of services in the background
    # this should be implementing abstract classes that define a clearly defined interface
    # so that various plug-ins can be used here
    def _deploy_to_executor(self, graph: OrchestrationGraph):
        """
        Implements the business logic to deploy the orchestration
        graph elements onto the backend
        
        This implementation is specific to the use of the AWSEventGrid
        API. 
        """
        # TODO Generalize the code with enhanced serverless abstraction semantics

        # For all subgraphs deploy the units
        for graph in self.subgraphs():
            # Creates a list of function objects to work on 
            func_objs = self.executor.Function.register([node.construct for node in graph.nodes.values()])
            # Link up the functions based on the edges
            for edge, params in graph.edges.items():
                start, target = edge
                # TODO Change this to a context managet to make the scope of the context clear
                with self.executor.Function.useFunction(start) as f:
                    assert f
                    f.triggers(target, params)
                    # TODO Ensure use function sets the context to utilize


            
