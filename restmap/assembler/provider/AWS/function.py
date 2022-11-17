"""
Implements the function interface for the BackendProvider 

Function
----------
AWS Lambda implementation
"""
import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
from 
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
        try:
            self._set_active_construct(self._constructs[name])
        except:
            pass
        # function = lambda_.Function(self._stack, 
            # id=name, 
            # code=code, 
            # handler=handler)
            self._set_active_construct(name)        
        return self
    
    def useFunction(self, uid:str):
        return self
    