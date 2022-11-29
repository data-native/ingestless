"""
Implmements an AWS native Orchestrator

Services used:
--------------
* EventGrid Scheduler
"""
from restmap.executor.BaseExecutor import BaseExecutor
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
    
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

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

        # For all subgraphs
        for graph in self.subgraphs():
            graph
        



