"""
Implmements an AWS native Orchestrator

Services used:
--------------
* EventGrid Scheduler
"""
from restmap.executor.AbstractBaseExecutor import AbstractBaseExecutor
from .BaseOrchestrator import BaseOrchestrator, OrchestrationGraph

# TODO Move this orchestrator out of AWS and implement as a generally available Orchestrator that is just dependent on the 
# Provider API. Enabling it to be orchestrating against any kind of backend.
class ServiceBusOrchestrator(BaseOrchestrator):
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
        
        Functionality:
        * Each resolution of a endpoint creates an "EndpointResolved" event with parameters detailing the resolver that finished
        * Each resolution of 
        """
        # For all subgraphs deploy the units
        for graph in self.subgraphs():
            # Register all executable nodes as functions in the executor 
            self.executor.Function.register([node.construct for node in graph.nodes.values()])
            # Create a topic in which to share success execution events across services
            self.executor.Topic.register('execution_success', {})
            # Link up the functions based on the edges using the provider service API to deploy the orchestration onto the backend
            for edge, params in graph.edges.items():
                start, target = edge
                # Tactic: Upstram sources publish status events into a shared topic, and all consumers subscribe to the topic using correctly parametrized filters 
                # the filter params can define the type of executable (resolver, endpoint, etc.) to enable subscribes to link directly to a successfull execution of a resolver function (example) 

                # TODO Later refactor to push the logic of retrieve or create into the provider class
                with self.executor.Topic.use('execution_success') as t:
                    # Configure start to emit an event on finish
                    with self.executor.Function.use(start) as f:
                        # target is set to be triggered on sns message
                        # TODO The function notifies on success to a topic. This configures the required permissions to publish on the topic and compiles the code for sending out the notification to the channel 
                        # in the function body, causing a likely recompile of the code files
                        # Allow the function to publish on the topic
                        t.grant_publish(f.get_active_construct())
                        # Recompile the code to publish the status event to the target topic
                        # This configures the event publishing code in the function
                        msg_params = {
                            'event_type': 'success',    
                            'on':['sucess', 'skipped'], # Should publish a success event on both successfull completion and when execution was skipped
                        }
                        f.trigger(on='success', source='topic', name='execution_success', args=msg_params)
                        # Can be called manually, or be set in the __exit__ function of the context manager
                        f.compile()
                    # Configure target to trigger on received event from start
                    with self.executor.Function.use(target) as f:
                        # Define the parameters for the event trigger here
                        trigger_params = {
                        }
                        f.trigger(on='topic', name='execution_success', args=trigger_params)
                        f.compile()
                        # Can be called manually, or be set in the __exit__ function of the context manager
    