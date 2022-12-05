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
from restmap.executor.AWS.AWSExecutor import AWSExecutor
from restmap.executor.AbstractBaseExecutor import AbstractBaseExecutor
from restmap.orchestrator.ServiceBusOrchestrator import ServiceBusOrchestrator

class Manager:
    """
        
    """

    def __init__(self, executor: str, name: str) -> None:

        self._parser = TemplateParser()
        self._state = State()
        self._resolver = Resolver()
        #TODO Extend to handle multiple compilation processes
        self._compiler= Compiler()
        self._executor = self._init_executor(executor, name)
        self._orchestrator = ServiceBusOrchestrator(executor=self._executor)
        self._deployables = []
    
    def _init_executor(self, executor: str, name: str) -> AbstractBaseExecutor:
        """Initializes the Provider instance for the chosen backend service"""
        if executor in ['aws', 'AWS']:
            return AWSExecutor(name)
        else:
            return f"No BackendProvider implemented for backend: {executor}"

    def validate(self, path: Union[str, Path]):
        """
        Validate the configuration files in the local environment
        """
        try:
            # Ensure they can be parsed correctly
            template_dict = self._parser.load(path)
            # Ensure the elements can be placed onto the graph
            execution_graph = self._resolver.resolve(template_dict)
        except Exception as e:
            # TODO Handle specific failure types and return instrumental error based on exception types
            print(f"The provided template is not valid. Failed with Exception: {e}")

    def plan(self, path: Union[str, Path]) -> StatusCode:
        """
        Loads, validates and parses the construct definition from the
        template file at the file location.

        Compiles and stores the validated deployment configuration
        for the given state in preparation for deployment.
        """
        # Load the template from the file path given
        template = self._parser.load(path)
        # Resolve template
        resolution_graph = self._resolver.resolve(template)
        # Store updated version
        self._state.state = resolution_graph
        # Computes the dependencies during execution
        orchestration_graph = self._orchestrator.orchestrate(deployables=compiled_deployables, resolution_graph=resolution_graph)
        # Compile the deployable assets
        compiled_deployables = self._compiler.from_orchestration_graph(orchestration_graph)
        # Create the stack in the IaC Executor
        self._orchestrator.deploy(self._deployables, dryrun=True)
        return StatusCode.SUCCESS

    def deploy(self, dryrun:bool = False):
        """
        Deploys the planend (resolved and compiled) elements onto
        the backend provider.

        @dryrun: Execute deployment procedure without actual deployment of infrastructure
        """
        #TODO Extend to handle a list of individual templates to deploy in one step
        # Validate that 
        if not self._deployables:
            # Try reading from set configuration location on default
            # Check that there is a difference to deploy
            # If not quit => 
            return "There is currently no planned deployment. Use `plan(template_path)` to register your templates" 

        else:
            # Conduct the actual deployment to the selected backend platform
            self._orchestrator.deploy(self._deployables, dryrun)
        
    def init(self):
        """
        Initialize the local environment 
        """
        # Create backend state

        # Load local files if any are present. Else fail
        
        raise NotImplementedError


        

        

        
        
    
