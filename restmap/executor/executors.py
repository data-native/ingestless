"""
This code registers the actual provider classes with
the abstract provider interface
"""
from .AbstractBaseExecutor import AbstractBaseExecutor
from .AWS import AWSExecutor

# Register all Executors implementing the interface__________
AbstractBaseExecutor.register(AWSExecutor)