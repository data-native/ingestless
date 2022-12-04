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
from typing import List, Union
import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_sns as sns
import aws_cdk.aws_lambda_event_sources as event_sources

from ..BaseConstructProvider import BaseConstructProvider
from restmap.compiler.function.FunctionCompiler import FunctionDeployment
from restmap.executor.AbstractBaseExecutor import AbstractBaseExecutor

@dataclass
class Function:
    """
    Implements the common abstraction interface for function objects
    within the framework
    """
    provider: BaseConstructProvider

class FunctionProvider(BaseConstructProvider):
    """
    Executes the constructs compiled by the Compile stage
    against the AWS lambda API. 

    Receives FunctionDeployment construct definitions.
    Compiles into AWS native CloudFormation stacks.
    """

    def __init__(self, executor: AbstractBaseExecutor, stack: cdk.Stack) -> None:
        super().__init__(stack)
        self.executor = executor

    def register(self, 
        function: Union[str, FunctionDeployment, List[FunctionDeployment]]) -> 'FunctionProvider':
        """
        Register one or more functions based on their specification
        """
        if isinstance(function, str):
            # Tries a retrieval of an existing function
            self._select_construct(function)
            return self

        # Attempt registration of the new functions
        # TODO Extend the parametrization 
        if not isinstance(function, list):
            function = [function]
            # Manage the case that the  
        func_objs = []
        for func_conf in function:
            try:
                func_obj = self._compile(function=func_conf)
                func_objs.append(func_obj)
                self._constructs[func_conf.uid] = func_obj
            except JSIIError:
                print(f"Construct {func_conf.uid} already present in the stack.")
                # return Topic(provider=self, topic=self._constructs[name])  
        return self

    # TODO Abstract the return object to be able to pass any kind of Serverless Function instead of just an AWS lambda SDK instance
    def notify(self, 
        target: str, 
        params: dict, 
        synchronous:bool=True,
        on:str='success',
        ) -> 'Function':
        """
        Chains the given functions execution to the previous
        execution of the other function. 

        Can optionally set the list of execution outcome statuses
        to trigger on. By default only triggers on successful execution.
        """
        #TODO Implement synch and asynch trigger mechanism
        # Ensure that a construct is set
        self._ensure_construct_scope()
        current = self.get_active_construct()
        try:
            target = self._constructs[target]
        except KeyError:
            raise KeyError(f"No funciton {target} registered in the system. Run `register` on the function prior to an scheduling attempt.")

        # Set the trigger on the target fuction to react to the chosen topic
        # request a new topic named after the function target, so that any other function can read from this
        # TODO Can likely be optimized to use build in filter on a shared "successfull execution" topic based on parameters (COST REDUCTION OPTION)
        return self
    
    def trigger(
        self,
        on: str,
        source: str,
        name: str,
        args: dict         
    ):
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

    def withRole(self, role:str) -> 'Function':
        """
        Assigns a role to the function
        Works against the active function construct
        """
        construct: lambda_.Function = self._construct_in_scope
        return self
    
    # INTERNAL API_________________
    def _compile(self, function: FunctionDeployment) -> lambda_.Function:
        """
        Creates a AWS Lambda based on the FunctionDeployment configuration
        """
        # Compile the passed code to a folder location to link the required artifacts into the docker compilation process in the CDK
        # TODO Store code file to target
        # TODO Create poetry.toml from requirements
        func_obj = lambda_.Function(self.stack, 
            id=function.uid, 
            code=lambda_.Code.from_asset(str(function.code_location.parent.absolute())),
            handler=function.handler,
            runtime=lambda_.Runtime(function.runtime),
            )
        return func_obj