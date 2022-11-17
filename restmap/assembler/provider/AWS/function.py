"""
Implements the function interface for the BackendProvider 

Function
----------
AWS Lambda implementation
"""
import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
from .BaseConstructProvider import BaseConstructProvider

class FunctionProvider(BaseConstructProvider):
    """
    Provides a builder interface for lambda instantiation
    """
    def __init__(self, stack: cdk.Stack) -> None:
        super().__init__(stack)
    
    def function(self, name: str, code: str) -> 'FunctionProvider':
        """
        Create a lambda function
        """
        if name in self._constructs:
            return self
        # function = lambda_.Function(self._stack, 
            # id=name, 
            # code=code, 
            # handler=handler)

        self._set_active_construct(name)        
    
    def useFunction(self, uid:str):
        
        if name in self._constructs: