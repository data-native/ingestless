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
from typing import List, Union
import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_sns as sns
from aws_cdk.aws_lambda_event_sources import SnsEventSource
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

    def withRole(self, role:str) -> 'Function':
        """
        Assigns a role to the function
        Works against the active function construct
        """
        construct: lambda_.Function = self.provider.selected_construct
        return self


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

    def register(self, function: Union[FunctionDeployment, List[FunctionDeployment]]) -> List['FunctionProvider']:
        """
        Register one or more functions based on their specification
        """
        if not isinstance(function, list):
            function = [function]
        func_objs = []
        for func_conf in function:
            func_obj = self.compile(function=func_conf)
            func_objs.append(func_obj)
            self._constructs[func_conf.uid] = func_obj
        return func_objs
        # Register dependencies amongst the functions

    # TODO Abstract the return object to be able to pass any kind of Serverless Function instead of just an AWS lambda SDK instance
    def compile(self, function: FunctionDeployment) -> 'FunctionProvider':
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
    
    def useFunction(self, function: str) -> 'FunctionProvider':
        """
        """
        return FunctionContextManager(self, function)
    

    def triggers(self, target: lambda_.Function, params: dict, synchronous:bool=True) -> 'Function':
        """
        Chains the given functions execution to the previous
        execution of the other function. 

        Can optionally set the list of execution outcome statuses
        to trigger on. By default only triggers on successful execution.
        """
        #TODO Implement synch and asynch trigger mechanism
        # Ensure that a construct is set
        assert self.selected_construct
        current = self.get_active_construct()

        # Set the trigger on the target fuction to react to the chosen topic
        # request a new topic named after the function target, so that any other function can read from this
        # TODO Can likely be optimized to use build in filter on a shared "successfull execution" topic based on parameters (COST REDUCTION OPTION)
        topic = self.executor.Topic.topic(current)
        # The code changes need to be applied on the function 
        # self.provider.
        
        # This is done natively in AWS CDK
        target.add_event_source(SnsEventSource(topic))
        return self

class FunctionContextManager:
    """
    
    """
    def __init__(self, provider: FunctionProvider, function: str) -> None:
        self.provider = provider
        self.selected_topic = function

    def __enter__(self) -> FunctionProvider:
        try:
            function = self.provider._constructs[self.selected_function]
            self.provider._select_construct(function)
            return Function(self.provider) 

        except KeyError:
            raise KeyError(f"No function {self.selected_function} registered. If configured, register the function with the Provider first.") 

    def __exit__(self):
        self.provider._select_construct = None