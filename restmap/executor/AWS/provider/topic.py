
"""
Implements the function interface for the BackendProvider Interace

All configuration required for definition, configuration and deployment
of the Messaging service are received through the standardized `ConstructDeployment` dataclass 
interfaces that are output from the `Compiler` stage.

Topic
----------
AWS SNS
"""
from dataclasses import dataclass
from jsii.errors import JSIIError
from typing import List, Union, Any
import aws_cdk as cdk
import aws_cdk.aws_sns as sns
from ..BaseConstructProvider import BaseConstructProvider

from restmap.executor.AbstractBaseExecutor import AbstractBaseExecutor

@dataclass
class Topic:
    """
    Implements the common abstraction interface for function objects
    within the framework
    """

    provider: BaseConstructProvider
    topic: sns.Topic

class TopicProvider(BaseConstructProvider):
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
        name: str,
        args: dict
    ) -> 'TopicProvider':
        """
        Create a topic to enable a pub/sub workflow within the application.
        If the topic is already defined, return it instead.
        """
        try:
            # TODO Extend the parametrization 
            topic = sns.Topic(self.stack, name)
            self._constructs[name] = topic
        except JSIIError:
            print(f"Construct {name} already present in the stack.")
            # return Topic(provider=self, topic=self._constructs[name])  
        return self

    def withRole(self, role:str) -> 'TopicProvider':
        """
        Assigns a role to the function
        Works against the active function construct
        """
        self._ensure_construct_scope()
        raise NotImplementedError
    
    # PRIVILEDGES__________
    def grant_publish(self, target) -> 'TopicProvider':
        """Allows the function to publish to the current topic"""
        self._ensure_construct_scope()
        self._construct_in_scope.grant_publish(target)
        return self

    