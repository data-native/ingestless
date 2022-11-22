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
from typing import Union
from pathlib import Path

from enums import StatusCode
from enums import Services
from restmap.manager.State import State
from restmap.templateParser.TemplateParser import TemplateParser, TemplateSchema
from restmap.resolver.Resolver import Resolver
from restmap.compiler.Compiler import Compiler
from restmap.
class Manager:
    """
    
    """

    def __init__(self) -> None:
        self._parser = TemplateParser()
        self._resolver = Resolver()
        #TODO Extend to handle multiple compilation processes
        self._compiler= Compiler()
        self._state = State()
        self._provider = 
        self._compiled_deployables = []
        
    def validate(self, path: Union[str, Path]):
        """
        Validate the configuration files in the local environment
        """
        # Ensure they can be parsed correctly
        template_dict = self._parser.load(path)
        # Ensure the elements can be placed onto the graph
        execution_graph = self._resolver.resolve(template_dict)

        raise NotImplementedError

    def plan(self, path: Union[str, Path]) -> StatusCode:
        """
        Registers a components defined in a given storage location
        """
        # Load the template from the file path given
        template = self._parser.load(path)
        # Resolve template
        resolution_graph = self._resolver.resolve(template)
        # Store updated version
        self._state.state = resolution_graph
        # Compile the deployable assets
        self._compiled_deployables = self._compiler.from_resolution_graph(resolution_graph)
        return StatusCode.SUCCESS

    def deploy(self):
        """
        Deploys the planend (resolved and compiled) elements onto
        the backend provider.
        """
        #TODO Extend to handle a list of individual templates to deploy in one step
        # Validate that 
        if not self._compiled_deployables:
            # Try reading from set configuration location on default
            # Check that there is a difference to deploy
            # If not quit => 
            return "There is currently no planned deployment. Use `plan(template_path)` to register your templates" 

        else:
            # Compile code for the function

            # Use the code to parametrize the function


    def init(self):
        """
        Initialize the local environment 
        """
        # Create backend state

        # Load local files if any are present. Else fail
        
        raise NotImplementedError


        

        

        
        
    
