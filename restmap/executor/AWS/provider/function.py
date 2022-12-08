"""
Implements the function interface for the BackendProvider Interace

All configuration required for definition, configuration and deployment
of the Lambda service are received through the standardized `ConstructDeployment` dataclass 
interfaces that are output from the `Compiler` stage.

Function
----------
AWS Lambda implementation
"""
from dataclasses import dataclass
from jsii.errors import JSIIError
from typing import List, Union, Dict
import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_sns as sns
import aws_cdk.aws_lambda_event_sources as event_sources

from ..BaseConstructProvider import BaseConstructProvider
from restmap.compiler.function.FunctionCompiler import FunctionDeployment 
from restmap.executor.AbstractBaseExecutor import AbstractBaseExecutor
from restmap.executor.AbstractTopicProvider import AbstractTopicProvider
from restmap.orchestrator.BaseOrchestrator import OrchestrationNode
from restmap.compiler.BaseCompiler import BaseCompiler
from restmap.compiler.function import FunctionCompiler

class BaseConstruct:
    """
    Base class for construct items returned from the ConstructProvider
    compilation process. 
    """
    pass

@dataclass
class Function(BaseConstruct):
    """
    Implements the common abstraction interface for function objects
    within the framework.

    It contains both the native, compiled IaC construct as well as the
    orginal orchestration node containing the parameters from the configuration.

    This enables the Function to act as a unit of deployment as well
    as the target for dynamic reconfiguration and recompilation processes.
    The recompilation is required to ensure that `Orchestrator` classes can dynamically
    recompile code logic in reaction to orchestration changes.
    """
    provider: 'FunctionProvider'
    construct: lambda_.Function 
    node: OrchestrationNode

    # All changes to 
    def write_to(self, sink:BaseConstruct) -> 'Function':
        """
        Adds an output target to the function.
        
        Adds an output node to the Function
        -> Result body should be output to the target
        """
        # TODO Add the output node to the function graph
        # Configure the output
        output_dict = {
        } 
        with self.compiler.use(self.node) as f: 
            f.function.output(
                 
                # Parametrize the output node
            )
        return self
    
    # Move this up to base construct to overwrite 
    @property
    def compiler(self) -> FunctionCompiler:
        return self.provider.executor._compiler

    def _recompile(self):
        """
        Recompiles the function code after updating it 
        """
        raise NotImplementedError
class FunctionProvider(BaseConstructProvider):
    """
    Executes the constructs compiled by the Compile stage
    against the AWS lambda API. 

    Receives FunctionDeployment construct definitions.
    Compiles into AWS native CloudFormation stacks.
    """

    def __init__(self, 
        executor: AbstractBaseExecutor, 
        stack: cdk.Stack) -> None:
        super().__init__(stack)
        self.executor = executor

    def register(self, 
        functions: Union[str, dict, List[dict]]
        ) -> 'FunctionProvider':
        """
        Register one or more functions based on their specification
        """
        if isinstance(functions, str):
            # Tries a retrieval of an existing function
            self._select_construct(functions)
            return self

        # Attempt registration of the new functions
        # TODO Extend the parametrization 
        if not isinstance(functions, list):
            functions = [functions]
            # Manage the case that the  
        func_objs = []
        for func_conf in functions:
            try:
                function_inst = self._compile(func_conf)
                func_objs.append(function_inst)
                self._constructs[function_inst.node.name] = function_inst
            except JSIIError:
                print(f"Construct {func_conf.construct.uid} already present in the stack.")
                # return Topic(provider=self, topic=self._constructs[name])  
        return self

    # TODO Abstract the return object to be able to pass any kind of Serverless Function instead of just an AWS lambda SDK instance
    def notify(self, 
        topic: Union[str, AbstractTopicProvider], 
        params: dict = {},
        synchronous:bool=True,
        on:str='success',
        payload:Dict ={},
        ) -> 'FunctionProvider':
        """
        Chains the given functions execution to the previous
        execution of the other function. 

        Can optionally set the list of execution outcome statuses
        to trigger on. By default only triggers on successful execution.
        """
        # Ensure that a construct is set
        self._ensure_construct_scope()
        function = self._construct_in_scope
        # Retrieve the target topic to get the details if passed by name string
        if isinstance(topic, str):
            try:
                topic = self._constructs[topic]
            except KeyError:
                raise KeyError(f"No topic {topic} registered in the system. Run `register` on the function prior to an scheduling attempt.")
        # Configure publication to the topic
        topic: AbstractTopicProvider = topic
        # TODO Find a way to place the attributes on the orchestration_graph 
        # Instruct the function to output to the target topic
        function.write_to(
            sink=topic
        )
        return self
    
    def trigger(
        self,
        on: str,
        source: str,
        name: str,
        args: dict         
    ) -> 'FunctionProvider':
        """
        Configures the function to trigger on an event_source.
        @event_source: Name of the construct type on which to react
        @name: Name of the actual event source instance in the specified construct class
        """
        # TODO refactor to reference a SST construct list for reference. This data is duplicated across the framework
        event_source_switch = {
            'topic': self.executor.Topic,
            'bucket': self.executor.Bucket,
            'queue': self.executor.Queue,
        }
        # TODO Make args optional so we can retrieve the construct easier
        # TODO register must return existing construct within active scope
        event_source = event_source_switch[source].register(name, args)

        # This registration needs to be provided by each implementation
        # to let the system know how the event routing should be translated onto the actual
        # backend system. 
        event_source_type = {
            'topic': event_sources.SnsEventSource,
            'bucket': event_sources.S3EventSource,
            'queue': event_sources.SqsEventSource,
        }
        # This is done natively in AWS CDK
        # TODO Register the event source for the given event types only (Or for all, depending on how this will work)
        self.get_active_construct().add_event_source(event_source_type[source](event_source.get_active_construct()))
        return self

    def withRole(self, role:str) -> 'FunctionProvider':
        """
        Assigns a role to the function
        Works against the active function construct
        """
        construct: lambda_.Function = self._construct_in_scope
        return self
    
    # INTERNAL API_________________
    def _compile(
            self, 
            node: dict
        ) -> lambda_.Function:
        """
        Creates a AWS Lambda based on the FunctionDeployment configuration
        """
        # Compile the passed code to a folder location to link the required artifacts into the docker compilation process in the CDK
        # TODO Store code file to target
        # TODO Create poetry.toml from requirements
        deployment, node = node['deployment'], node['node']
        func_obj = lambda_.Function(self.stack, 
            id=deployment.uid, 
            code=lambda_.Code.from_asset(str(deployment.code_location.parent.absolute())),
            handler=deployment.handler,
            runtime=lambda_.Runtime(deployment.runtime),
            )
        # This wrapped response enables recompilation and dynamic parametrization 
        # of the deployable function construct within the Orchestrator
        response = Function(
            provider=self,
            node=node,
            construct=func_obj,     
        )
        return response