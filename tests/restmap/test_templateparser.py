"""
Tests the templateparser implementation
"""

import pytest
import json
import yaml
from pathlib import Path
from restmap.templateParser.TemplateParser import TemplateParser, TemplateSchema, MetadataDict, ConfigurationDict
from enums import StatusCode 

# FIXTURES
@pytest.fixture()
def parser():
    return TemplateParser()

@pytest.fixture()
def template_path():
    return Path('./tests/restmap/assets/complex_endpoint.yml')
    # Write file to templocation
    # return templocation

# TESTS________________
def test_validate(parser: TemplateParser, template_path: Path):
    file = template_path.read_text()
    template_string = yaml.safe_load(file)
    parser._validate(template_string)

def test_load(parser: TemplateParser, template_path):
    # Create temp file
    template = parser.load(template_path)
    assert isinstance(template, TemplateSchema)
    assert isinstance(template.metadata, MetadataDict)
    assert isinstance(template.config, ConfigurationDict)


def test_logic(parser: TemplateParser, template_path):
    # Create an endpoint template

    parser.load(template_path)
    # ``