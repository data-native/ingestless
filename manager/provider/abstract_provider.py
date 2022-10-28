"""
Backend Utility functions
-------------------------

Services to enable the coordination with the 

"""
from abc import ABC, abstractmethod
from configparser import ConfigParser
from multiprocessing.sharedctypes import Value
from typing import List


class BackendProvider(ABC):
    """
    General class managing the interaction with the backend provider
    """

    def __init__(self) -> None:
        self.parser = ConfigParser()
        self.clients = {}
    
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

    # Working_with_services__________-
    @abstractmethod
    def _initialize_client(self, client:str) -> None:
        raise NotImplementedError

