"""
NOT YET IMPLEMENTED

Implements the table interface for the BackendProvider 

Table
----------
AWS DynamoDB
"""
import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dydb
from ..BaseConstructProvider import BaseConstructProvider

#TODO Implement the Provider

class TableProvider(BaseConstructProvider):
    """
    Provides a builder interface for queue instances
    
    Builds resources onto a given stack
    """
    #TODO: Complete implementation of method API

    def __init__(self, stack: cdk.Stack) -> None:
        super().__init__(stack)

    def table(self, name: str='') -> 'TableProvider':
        """
        Create a new queue
        """
        raise NotImplementedError
    
    def use_table(self, uid: str) -> 'TableProvider':
        """Uses an existing bucket for further configuration"""
        # Assumes bucket is in same account
        if uid in self._constructs:
            self._active_construct = self._constructs[uid] 
        else:
            pass
        return self
    
    def withRole(self, role:str) -> 'TableProvider':
        """"""
        raise NotImplementedError
    