"""
Tests the templateparser implementation
"""

import pytest
import json
from restmap.templateParser.TemplateParser import TemplateParser, TemplateSchema
from manager.enums import StatusCode

# FIXTURES
@pytest.fixture()
def parser():
    return TemplateParser()

@pytest.fixture()
def template_path():
    # Get temporary location
    schema = {
        #Define schema
    }
    schema_str = json.dumps(schema)
    # Write file to templocation
    # return templocation

# TESTS________________
def test_load(parser: TemplateParser, template_path):
    # Create temp file
    template = parser.load(template_path)
    assert isinstance(template, TemplateSchema)


def test_logic(parser: TemplateParser, template_path):
    # Create an endpoint template

    # ``
    parser.load()