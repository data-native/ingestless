import pytest

from typer.testing import CliRunner

from manager.database import DatabaseHandler
from manager.enums import StatusCode
from manager.manager import Manager
from manager.provider.AWSProvider import AWSProvider

@pytest.fixture
def local_manager(local_db):
    return Manager() 

@pytest.fixture
def AwsProvider():
    return AWSProvider()

def test_is_configured(AwsProvider):
    assert AwsProvider.is_configured()
    
def test_get_configuration(AwsProvider):
    config = AwsProvider.get_configuration()
    assert config

def test_get_profiles(AwsProvider):
    profiles = AwsProvider.get_profiles()
    assert isinstance(profiles, list)

def test_switch_profile(AwsProvider):
    profiles = AwsProvider.get_profiles()
    for p in profiles:
        AwsProvider.switch_profile(p)
        assert AwsProvider.session.profile_name == p

# TEST_Function_handler
def test_list_functions(AwsProvider):
    functions = AwsProvider.list_functions()
    assert isinstance(functions, dict)
    assert 'Functions' in functions