import pytest

from typer.testing import CliRunner
from typing import List
from botocore import client as botoclient

from manager.models import FunctionModel
from manager.database import DatabaseHandler
from manager.enums import StatusCode, Services
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

def test_get_client(AwsProvider):
    for service in Services:
        client = AwsProvider.get_client(service)
        assert isinstance(client, botoclient.BaseClient)

# TEST_Function_handler
def test_list_functions(AwsProvider):
    functions = AwsProvider.list_functions()
    assert isinstance(functions, list)
    # assert all([isinstance(function, botocore.client.lambda) for function in functions])

# EVENTS________________
def test_describe_rule(AwsProvider: AWSProvider):
    name = 'testrule'
    rule = AwsProvider.describe_rule(name=name)
    # assert all([name in rule for name in ['Name', 'Arn', 'EventPattern', 'State', 'Description'] ])

def test_disable_rule(AwsProvider):
    raise NotImplementedError

def test_enable_rule(AwsProvider):
    raise NotImplementedError

def test_list_rules_by_target(AwsProvider):
    raise NotImplementedError

def test_list_rules(AwsProvider):
    raise NotImplementedError

def test_list_targets_by_rule(AwsProvider):
    raise NotImplementedError

def test_put_permissions(AwsProvider):
    raise NotImplementedError

def test_put_rule(AwsProvider):
    rule = {
        'Name': 'Testrule',
        'ScheduleExpression': 'cron(* * * * *)',
        'State': 'DISABLED',
        'Description': 'A sample rule',
    }
    AwsProvider.put_rule(rule)

def test_put_targets(AwsProvider):
    raise NotImplementedError