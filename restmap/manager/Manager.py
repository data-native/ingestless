"""
RestMap Manager

The class provides the management API enabling the initializion
of a local project state, the validation of templates, the registration
of components based on the templates and the management and display of 
the application state.

Overall target is to achieve a highly flexible definition and workflow
management for complex REST API integration processes.

This class relays all functionality to provider classes that house
the business and technical logic.

Overall, the implementation in the RestMap service is independent of 
actual deployment details on a specific backend provider, by compiling all 
activities into the overall serverless abstraction syntax used across the
ingestless framework.
"""
from typing import Union, AnyStr
from pathlib import Path

from manager.State import State
from templateParser.TemplateParser import TemplateParser, TemplateSchema
class Manager:

    def __init__(self) -> None:
        self._parser = TemplateParser()
        self.state = State()
        
    def register(self, path: Union[str, Path]) -> None:
        """
        Registers a components defined in a given storage location
        """
        # Load the template from the file path given
        component = self._parser.load(path) 
        
        # Add component to local state
        self.state._add(component)
    
    def validate(self):
        """
        Validate the configuration files in the local environment
        """
        raise NotImplementedError

    def describe(self, component: str) -> AnyStr:
        """
        Compiles a description of the component for introspection
        """
        # Prepare the attribute filter

        # Get component from state
        component = self.state._get(component)
    
    def init(self):
        """
        Initialize the local environment 
        """
        # Create backend state

        # Load local files if any are present. Else fail
        
        raise NotImplementedError


        

        

        
        
    
