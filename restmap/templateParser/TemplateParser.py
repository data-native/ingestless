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

from utils import io as ioutils

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
        path = ioutils.ensure_path(path)
        # Load the file
        try:
            file = path.read_text() 

            if self.lints(file):
                schema = self._validate(file)
                template = self._parse(schema)
                # Load all components and lint component schemata
                for k,v in template.items():
                    template[k] = self.compile_component(component=k, attributes=v)
        except FileNotFoundError:
            return StatusCode.File
        # Lint the content string
        # Validate required components are defined
                
        return TemplateSchema()

    # INTERNAL API_______________-
    def _read_file(path: Path) -> File:
        """
        """
    
