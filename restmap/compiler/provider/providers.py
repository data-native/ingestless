"""
This code registers the actual provider classes with
the abstract provider interface
"""
from .BaseProvider import BaseBackendProvider
from .AWS import AWSProvider

BaseBackendProvider.register(AWSProvider)