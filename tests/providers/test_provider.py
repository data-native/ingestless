import json
import pytest

from typer.testing import CliRunner

from manager.database import DatabaseHandler
from enums import StatusCode, Provider
from manager.manager import Manager
from manager.provider.AWS.AWSProvider import AWSProvider 

@pytest.fixture
def local_manager(local_db):
    return Manager() 

@pytest.fixture
def AwsProvider():
    return AWSProvider()

def test_is_configured(AwsProvider):
    assert AwsProvider.is_configured()
    
def test_aws_get_configuration(AwsProvider):
    config = AwsProvider.get_configuration()
    assert config

def test_aws_get_profiles(AwsProvider):
    profiles = AwsProvider.get_profiles()
    assert isinstance(profiles, list)

def test_aws_switch_profile(AwsProvider):
    profiles = AwsProvider.get_profiles()
    for p in profiles:
        AwsProvider.switch_profile(p)
        assert AwsProvider.session.profile_name == p

# TEST 