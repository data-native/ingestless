
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

    def withRole(self, role:str) -> 'Topic':
        """
        Assigns a role to the function
        Works against the active function construct
        """
        return self
    
    def grant_publish(self, target):
        """Allows the function to publish to the current topic"""
        self.topic.grant_publish(target)
        return self

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
   
    def register(self, topic) -> List['TopicProvider']:
        """
        Register one or more functions based on their specification
        """
        # TODO Can potentially become required when a parametrized deployable instance is defined in the template. But not likely
        raise NotImplementedError

    # TODO Rewrite for Topic handling
    def compile(self, function) -> 'TopicProvider':
        """
        Creates a AWS Lambda based on the FunctionDeployment configuration
        """
        raise NotImplementedError
    
    def topic(self,
        name: str,
        args: dict
    ) -> Topic:
        """
        Create a topic to enable a pub/sub workflow within the application.
        """
        topic = sns.Topic(self.stack, name)
        self._constructs[name] = topic
        return Topic(provider=self, topic=topic)

    def use_topic(self, topic: str) -> 'TopicProvider':
        return TopicContextManager(provider=self, topic=topic)
    
    
    
class TopicContextManager:
    """
    
    """
    def __init__(self, provider: TopicProvider, topic: str) -> None:
        self.provider = provider
        self.selected_topic = topic

    def __enter__(self) -> TopicProvider:
        try:
            topic = self.provider._constructs[self.selected_topic]
            self.provider._select_construct(topic)
            return self.provider 

        except KeyError:
            raise KeyError(f"No function {self.selected_topic} registered. If configured, register the function with the Provider first.") 

    def __exit__(self, exception_type, exception_value, traceback):
        self.provider.selected_construct = None