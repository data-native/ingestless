
"""
Implements the function interface for the BackendProvider Interace

All configuration required for definition, configuration and deployment
of the Messaging service are received through the standardized `ConstructDeployment` dataclass 
interfaces that are output from the `Compiler` stage.

Topic
----------
AWS SNS
"""
from typing import List, Union
import aws_cdk as cdk
import aws_cdk.aws_sns as sns
from ..BaseConstructProvider import BaseConstructProvider

from restmap.executor.AbstractBaseExecutor import AbstractBaseExecutor

class TopicProvider(BaseConstructProvider):
    """
    Executes the constructs compiled by the Compile stage
    against the AWS lambda API. 

    Receives FunctionDeployment construct definitions.
    Compiles into AWS native CloudFormation stacks.
    """

    def __init__(self, executor: AbstractBaseExecutor, stack: cdk.Stack) -> None:
        super().__init__(stack)
   
    def register(self, topic) -> List['TopicProvider']:
        """
        Register one or more functions based on their specification
        """
        raise NotImplementedError
        # Register dependencies amongst the functions

    def compile(self, function) -> 'TopicProvider':
        """
        Creates a AWS Lambda based on the FunctionDeployment configuration
        """
        raise NotImplementedError
    
    def use_topic(self, function: str) -> 'TopicProvider':
        """
        """
        raise NotImplementedError
    
    def withRole(self, role:str) -> 'TopicProvider':
        """
        Assigns a role to the function
        Works against the active function construct
        """
        raise NotImplementedError

    def triggers(self, target: sns.CfnTopic, params: dict):
        """
        Chains the given functions execution to the previous
        execution of the other function. 

        Can optionally set the list of execution outcome statuses
        to trigger on. By default only triggers on successful execution.
        """
        raise NotImplementedError
