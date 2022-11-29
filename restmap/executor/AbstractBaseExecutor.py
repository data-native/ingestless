"""
The BaseProvider defines the 
interface to implement for a chosen
backend provider to be supported as a
compilation target.

Provider
-----------
A provider is a service platform that provides
full cloud service stacks on-demand through
a REST API, such as AWS, Azure, GCP, or Kubernetes
targets.

Service
-----------
A service represents an abstracted servless component
offering that can be implemented through a variety
of native services on the chosen backend provider. 

The system uses the abstraction of:
* Function: To define a serverless compute offering
* Table: To define a serverless, tabular storage service
* Queue: As a serverless storage and distribution medium for
         messages.
* Bucket: To define a BLOB storage medium
* 
"""
from abc import ABC, abstractclassmethod, abstractstaticmethod, abstractproperty, abstractmethod
from restmap.orchestrator.OrchestrationGraph import OrchestrationGraph
from restmap.executor.AWS.provider.function import FunctionProvider
from restmap.executor.AWS.provider.bucket import BucketProvider
from restmap.executor.AWS.provider.queue import QueueProvider
from restmap.executor.AWS.provider.table import TableProvider

#TODO: Check if implementation as ABC makes sense here
class AbstractBaseExecutor(ABC):
    """
    The generalized integration Interface
    to enable the communication between the
    assembler and the backend service.
    """

    @abstractmethod
    def Function(self) -> FunctionProvider:
        """
        Create a function in the system
        """

    @abstractmethod
    def Bucket(self) -> BucketProvider:
        """
        Create a BLOB storage bucket in the system
        """

    @abstractmethod
    def Table(self) -> TableProvider:
        """
        Create a storage table
        """
    
    @abstractmethod
    def Queue(self) -> QueueProvider:
        """
        Create a storage queue
        """

    @abstractmethod
    def Topic(self) -> TopicProvider:
        """
        Create a notification/messaging topic
        """

    @abstractmethod
    def compile(self, graph: OrchestrationGraph):
        """
        Create a storage table
        """

    @abstractmethod
    def deploy(self):
        """
        Create a storage table
        """

    @abstractmethod
    def diff(self, update):
        """
        """

    @abstractmethod
    def tear_down(self):
        """
        """

    @abstractmethod
    def diff(self, update):
        """
        """