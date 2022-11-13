"""
Template Parser

Enables the YAML based declarative definition of resources to be created
and managed by the RestMap framework. 

Along the lines of the Kubernetes API, the files can be stored in a local
folder structure and parsed using this class.

It drives the file input, linting, structure parsing, component validation
and class conversion of the read attributes into schema elements to be exported
further for scheduling.
"""

from pathlib import Path
from typing import Union, List, Dict


class TemplateSchema:
    """
    Defines the base class for the component schema classes
    """
    

class TemplateParser:
    """
    Implements the parser interface
    """

    def __init__(self) -> None:
        pass       
    
    # PUBLIC API______________
    def load(self, path: Union[str, Path]) -> TemplateSchema:
        """
        Attempts to verify and load a Template from a given file location.
        """
        # Load the file

        # Lint the content string

        # Validate required components are defined

        # Load all components and lint component schemata

        # Return TemplateSchema
        raise NotImplementedError

    
    