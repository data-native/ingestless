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

def test_list_rules(AwsProvider: AWSProvider):
    response = AwsProvider.list_rules()
    rules = response['Rules']
    assert isinstance(rules, list)
    assert all([name in rules[0] for name in ['Name', 'Arn', 'State', 'Description', 'ScheduleExpression', 'EventBusName']])

def test_list_targets_by_rule(AwsProvider):
    raise NotImplementedError

def test_put_permissions(AwsProvider):
    raise NotImplementedError

def test_put_rule(AwsProvider):
    rule = {
        'Name': 'Testrule',
        'ScheduleExpression': 'rate(5 minutes)',
        'State': 'DISABLED',
        'Description': 'A sample rule',
    }
    response: str = AwsProvider.put_rule(rule)
    assert isinstance(response, str)
    assert response.startswith('arn:aws')
    assert response.endswith(rule['Name'])

def test_put_targets(AwsProvider: AWSProvider):
    """
    Ensures the following targets can be added
    as execution targets for a defined schedule
    rule in EventBus
    
    * AWS Lambda, AWS Step Functions, AWS Batch Job, SNS, SQS
    """

    functions = AwsProvider.list_functions()
    rule_name = 'Testrule'
    targets = []
    response = AwsProvider.put_targets(
        rule=rule_name,
        targets=targets,
    )
    return response

def test_put_target_function(AwsProvider: AWSProvider):
    """
    Tests that a function target can be associated
    to a given rule on the ServiceBus 
    """
    from manager.types import EventTargetItem
    rule_name="Testrule"
    functions = AwsProvider.list_functions()
    response = AwsProvider.put_target(
        rule=rule_name,
        type=Services.Function,
        target=functions[0]
    )
    assert response

def test_describe_rule(AwsProvider: AWSProvider):
    """
    Ensures details about a rule can be retrieved 
    by name of the given rule on the selected ServiceBus
    """
    rule_name = 'Testrule'
    rule = AwsProvider.describe_rule(name=rule_name)
    assert isinstance(rule, dict)
    assert all([n in rule for n in ['Name', 'Arn', 'ScheduleExpression', 'State', 'Description', 'EventBusName', 'CreatedBy']])
        
def test_enable_rule(AwsProvider: AWSProvider):
    """
    Ensure you can enable a disabled rule
    """
    rule_name = 'Testrule'
    response = AwsProvider.enable_rule(name=rule_name)
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200
    
    rule = AwsProvider.describe_rule(name=rule_name)
    assert rule['State'] == 'ENABLED'

def test_disable_rule(AwsProvider: AWSProvider):
    """
    Ensure you can disable an enabled rule
    """
    rule_name = 'Testrule'
    response = AwsProvider.disable_rule(name=rule_name)
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200
    
    rule = AwsProvider.describe_rule(name=rule_name)
    assert rule['State'] == 'DISABLED'