"""
Backend Utility functions
-------------------------

Services to enable the coordination with the 

"""
from abc import ABC, abstractmethod
from configparser import ConfigParser
from multiprocessing.sharedctypes import Value
from typing import Optional, List, TypeVar
import logging

from manager.enums import Provider
import boto3

class BackendProvider(ABC):
    """
    General class managing the interaction with the backend provider
    """

    def __init__(self) -> None:
        self.parser = ConfigParser()
    
    @classmethod
    def new(cls, provider: Provider):
        """
        Factory pattern for subclasses
        """
        provider_switch = {
            Provider.AWS : AWSProvider,
            # Provider.AZURE : AzureProvider,
            # Provider.GCP : GCPProvider,
            # Provider.CLOUDNATIVE : CloudNativeProvider
        }
        return provider_switch[provider]()
    
    @abstractmethod
    def get_profiles(self) -> List:
        """Retrieves the list of available profiles"""
        pass

    @abstractmethod
    def switch_profile(self, profile: str) -> None:
        """Switches to a given profile"""
        raise NotImplementedError
    
    @abstractmethod
    def get_region(self) -> None:
        """Retrieves the current region"""
        raise NotImplementedError

    @abstractmethod
    def is_configured(self) -> bool:
        """Tests if configuration is provided"""
        raise NotImplementedError
    
    @abstractmethod
    def get_configuration(self) -> None:
        """
        Retrieve the local configuration for the backend provider
        """
        raise NotImplementedError
    
    @abstractmethod
    def set_local_configuration(self):
        """
        
        """
        raise NotImplementedError

    
class AWSProvider(BackendProvider):
    """
    AWS Backend provider implementation
    """
    def __init__(self, profile:str='') -> None:
        self.profile = None 
        self.session= boto3.Session(profile_name=profile) if profile !='' else boto3.Session()
        super().__init_subclass__()

    def is_configured(self) -> bool:
        return self.session is not None

    def get_configuration(self):
        # Check if aws credentials are set
        credentials = self.session.get_credentials()
        return credentials
    
    def get_profiles(self) -> List:
        profiles = self.session.available_profiles
        return profiles
    
    def switch_profile(self, profile: str) -> None:
        profiles = self.get_profiles()
        if not profile in profiles:
            raise ValueError(f'Profile: {profile} not set. Available: {profiles}')
        self.session = boto3.Session(profile_name=profile) 

    def list_functions(self) -> None:
        pass

    def set_local_configuration(self):
        return super().set_local_configuration()
    
    def get_region(self) -> None:
        return super().get_region()

    
# class AzureProvider(BackendProvider):
    # pass

# class GCPProvider(BackendProvider):
    # pass

# class CloudNativeProvider(BackendProvider):
    # pass