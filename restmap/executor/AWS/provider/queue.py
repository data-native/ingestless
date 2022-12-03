
"""
NOT YET IMPLEMENTED

Implements the queue interface for the BackendProvider 

Bucket
----------
AWS SQS
AWS EventGrid
"""
import aws_cdk as cdk
import aws_cdk.aws_sqs as sqs
from ..BaseConstructProvider import BaseConstructProvider

#TODO Implement the Provider

class QueueProvider(BaseConstructProvider):
    """
    Provides a builder interface for queue instances
    
    Builds resources onto a given stack
    """
    #TODO: Complete implementation of method API

    def __init__(self, stack: cdk.Stack) -> None:
        super().__init__(stack)

    def queue(self, name: str='') -> 'QueueProvider':
        """
        Create a new queue
        """
        raise NotImplementedError
    
    def use_queue(self, uid: str) -> 'QueueProvider':
        """Uses an existing bucket for further configuration"""
        # Assumes bucket is in same account
        if uid in self._constructs:
            self._active_construct = self._constructs[uid] 
        else:
            pass
        return self
    
    def withRole(self, role:str) -> 'QueueProvider':
        """"""
        raise NotImplementedError
    