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

from dataclasses import dataclass, field
import jsonschema
from utils import io as ioutils
from enums import StatusCode

@dataclass
class MetadataDict:
    name: str = ''
    tags: list[str] = field(default_factory=list)

@dataclass 
class ConfigurationDict:
    endpoints: dict
    params: dict 
    resolvers: dict
@dataclass
class TemplateSchema:
    """
    Defines the base class for the component schema classes
    """
    version: str
    kind: str
    metadata: MetadataDict
    config: ConfigurationDict

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
        # TODO: 
        try:
            template_dict = self._read_template_file(path)
            # Validate required components are defined. Raises if it fails
            self._validate(template_dict)
            # Load all components and lint component schemata
            template: TemplateSchema = self._parse(template_dict)
            return template
        except FileNotFoundError:
            raise FileNotFoundError("The file provided does not exist")

    # INTERNAL API_______________-
    def _read_template_file(self, path: Path):
        """
        Reads the given file, ensures it is valid yaml and loads it
        """
        import yaml
        file = path.read_text()
        template_dict = yaml.safe_load(file)
        return template_dict
        
    def _validate(self, template_dict: dict) -> bool:
        """
        Ensure the file template confirms with expected
        file schema
        @template_string: Parsed dict from yaml input
        """
        from restmap.templateParser.schemata import schema_mapping
        # Validate overall schema first
        try:
            jsonschema.validate(template_dict, schema_mapping['template'])
            for key, values in template_dict.items():
                if key in schema_mapping:
                    jsonschema.validate(values, schema_mapping[key])
        except jsonschema.ValidationError as e:
            raise e
        return True

    def _parse(self, template_dict: dict ) -> TemplateSchema:
        """
        Parse a yaml template string into a TemplateSchema instance
        
        Does currently hardcode the structure of the expected template
        schema. 
        """
        #TODO: Generalize to support multiple versions of template schema
        # Input is a yaml template file string
        metadata_dict = MetadataDict(template_dict['metadata'])
        config_dict = ConfigurationDict(**template_dict['config'])
        template_dict['metadata'] = metadata_dict
        template_dict['config'] = config_dict
        return TemplateSchema(
            **template_dict
        )
