"""
Validates the RestMap Manager API responsible for
the validation, planning, compilation and deployment interaction
based on a yml template configuration. 
"""
import pytest
from pathlib import Path
from restmap.manager.Manager import Manager

@pytest.fixture
def manager():
    return Manager('stackname', 'AWS')

@pytest.fixture
def template_path():
    return Path('./ingestless/tests/restmap/assets/complex_endpoint.yml')
    # Write file to templocation

def test_can_plan(template_path: Path, manager: Manager):
    manager.plan(template_path)
    

def test_can_validate(template_path: Path, manager: Manager):
    # with pytest.raises():
        # manager.deploy()
    manager.plan(template_path)
    manager.deploy(dryrun=True)