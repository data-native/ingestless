"""
This code registers the actual provider classes with
the abstract provider interface
"""
from .BaseExecutor import BaseExecutor
from .AWS import AWSExecutor

BaseExecutor.register(AWSExecutor)