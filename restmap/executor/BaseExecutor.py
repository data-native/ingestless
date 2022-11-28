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
#TODO: Check if implementation as ABC makes sense here
class BaseExecutor(ABC):
    """
    The generalized integration Interface
    to enable the communication between the
    assembler and the backend service.
    """

    @abstractmethod
    def function(self):
        """
        Create a function in the system
        """
    @abstractmethod
    def table(self):
        """
        Create a storage table
        """


