"""
Implements the function interface for the BackendProvider Interace

All configuration required for definition, configuration and deployment
of the Lambda service are received through the standardized `ConstructDeployment` dataclass 
interfaces that are output from the `Compiler` stage.

Function
----------
AWS Lambda implementation
"""
from typing import List, Union
import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
from .BaseConstructProvider import BaseConstructProvider
from restmap.compiler.function.FunctionCompiler import FunctionDeployment
class FunctionProvider(BaseConstructProvider):
    """
    Executes the constructs compiled by the Compile stage
    against the AWS lambda API. 

    Receives FunctionDeployment construct definitions.
    Compiles into AWS native CloudFormation stacks.
    """

    def __init__(self, stack: cdk.Stack) -> None:
        super().__init__(stack)
   
    def register(self, function: Union[FunctionDeployment, List[FunctionDeployment]]) -> List['FunctionProvider']:
        """
        Register one or more functions based on their specification
        """
        if not isinstance(function, list):
            function = [function]
        func_objs = []
        for func_conf in function:
            func_obj = self.function(function=func_conf)
            func_objs.append(func_obj)
        return func_objs
        # Register dependencies amongst the functions

    def function(self, function: FunctionDeployment) -> 'FunctionProvider':
        """
        Creates a AWS Lambda based on the FunctionDeployment configuration
        """
        
        # Compile the passed code to a folder location to link the required artifacts into the docker compilation process in the CDK
        # TODO Store code file to target
        # TODO Create poetry.toml from requirements
        # TODO 
        lambda_.Runtime

        func_obj = lambda_.Function(self._stack, 
            id=function.uid, 
            code=lambda_.Code.from_asset(function.code), 
            handler=function.handler,
            runtime=lambda_.Runtime(function.runtime),
            )
        #TODO Change up the Runtime

        self._set_active_construct(func_obj)

        return self
    
    def withRole(self, role:str) -> 'FunctionProvider':
        """
        Assigns a role to the function
        Works against the active function construct
        """
        return self

    def triggers(self, target: lambda_.Function, params: dict):
        """
        Chains the given functions execution to the previous
        execution of the other function. 

        Can optionally set the list of execution outcome statuses
        to trigger on. By default only triggers on successful execution.
        """
        # Ensure that a construct is set
        assert self._selected_construct()
        current = self._get_active_construct()
        # Trigger the target function through the current function
        target.add_event_source(source=target)


    def useFunction(self, uid:str):
        raise NotImplementedError
        # Retrieve the function a
        self._set_active_construct()
        return self
    
    