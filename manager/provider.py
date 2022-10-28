"""
Backend Utility functions
-------------------------

Services to enable the coordination with the 

"""
from configparser import ConfigParser
from typing import Optional, List
import logging

from manager.enums import Provider
from manager.provider import BackendProvider


class BackendProvider:
    """
    General class managing the interaction with the backend provider
    """

    def __init__(self) -> None:
        self.parser = ConfigParser()
    
    @classmethod
    def new(cls, provider: Provider) -> BackendProvider:
        """
        Factory pattern for subclasses
        """
        provider_switch = {
            Provider.AWS : AWSProvider,
            Provider.AZURE : AzureProvider,
            Provider.GCP : GCPProvider,
            Provider.CLOUDNATIVE : CloudNativeProvider
        }
        return provider_switch[provider]()

    def local_configuration(self) -> None:
        """
        Retrieve the local configuration for the backend provider
        """
        raise NotImplementedError
    
    def set_local_configuration(self):
        """
        
        """
        raise NotImplementedError

    
    


class AWSProvider(BackendProvider):
    """
    AWS Backend provider implementation
    """

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def local_configuration(self) -> Optional[dict]:
        # Check if aws credentials are set
        try:
            credentials = self.parser.read('~/.aws/credentials')
        except:
            logging.debug("No AWS credentials set locally")
        try:
            config = self.parser.read('~/.aws/config')
        except:
            logging.debug("No AWS config set locally")
        return 

        return {}

class AzureProvider(BackendProvider):
    pass

class GCPProvider(BackendProvider):
    pass

class CloudNativeProvider(BackendProvider):
    pass