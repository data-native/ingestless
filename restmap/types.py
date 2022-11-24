"""
Datatypes used within the RestMap component
"""
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import AnyStr, ByteString, Dict, List, Optional, Union


class Entity(ABCMeta):
    """
    Interface for Entity instance definitions.

    An entity represents the abstract base class for 
    all managed types of objects to be registered and 
    maintained throughout rest ingestion.
    
    The implementing classes define the interface for the
    objects to interact with the management, and scheduling
    components.
    """
    @abstractmethod
    def resolve():
        pass

class TemplateSchema(ABCMeta):
    """
    Interface for TemplateSchemata defintions.
    
    A TemplateSchema carries the validation logic for 
    its associated object class and provides export
    methods to compile the schema for further usage.
    """

    @abstractmethod
    def parse() -> Entity:
        """
        Parses the given schema into the corresponding Entity instance 
        """
        pass

class Endpoint:
    """
    A Endpoint instance carries the ingestion logic
    for a given REST service endpoint.
    """
    def resolve(self):
        return True

    


@dataclass
class RestTemplate:

    def __init__(self, configuration: dict) -> None:
        #TODO: Set the expected schema for the Rest Entity type
        self._schema = None
        self._config = self.validate(configuration)


    def parse() -> Endpoint:
        # Parse self._schema into a RestEntity Instance
        return Endpoint()
    
    def validate(self, config: dict) -> dict:
        """
        Validates the configuration dictionary against
        the Object type schema in the set template version.
        """
        # VAlidate against the set schema

        # Raise error when validation fails
        raise NotImplementedError 
    
    def display_validation_error(self) -> None:
        """
        Compiles an informative validation error return
        statement to guide the user how to fix the schema
        definition.
        """ 
        raise NotImplementedError 
    