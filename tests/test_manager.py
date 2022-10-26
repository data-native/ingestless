import json
import pytest

from typer.testing import CliRunner

from manager.database import DatabaseHandler
from manager.enums import StatusCode
from manager.manager import Manager


@pytest.fixture
def local_db():
    #TODO: Create connection to local DynamoDB instance
    #TODO: Initialize the local db with table schema
    #TODO: Place a starting set of data in local db
    return DatabaseHandler() 

@pytest.fixture
def local_manager(local_db):
    return Manager() 


@pytest.fixture
def mock_json_file(tmp_path):
    functions = {
        "lambda_1": {
            "name": "lambda 1",
            "arn": "aws::lambda::lambda1.eu-west.lambda.aws.com",
        }
    }
    db_file = tmp_path / "registered_functions.json"
    with db_file.open('w') as db:
        json.dump(functions, db, indent=4)
    return db_file


test_data1 = {
    "function_name": "lambda_1",
    "body": {
        "name": "test"
    },
}
@pytest.mark.parametrize(
    "function_name, body, expected",
    [
        pytest.param(
            test_data1["function_name"],
            test_data1["body"],
            (test_data1["body"], StatusCode.SUCCESS)
        )
    ]
)
def test_register_functions(local_manager, function_name, body, expected):
    status = local_manager.register_lambda(function_name, body)
    assert isinstance(status, dict) 
    assert isinstance(status["status"], StatusCode)


def test_unregister_function(local_manager):
    local_manager.unregister_lambda('testlambda')

def test_list_functions(local_manager):
    functions = local_manager.list_lambdas()

def test_register_schedules(local_manager):
    test_schedules = [{}]
    schedules = local_manager.register_schedules()

@pytest.mark.parametrize(
    "schedule_name, expected",
    [
        pytest.param(
            "testschedule",
            {
                "name": "testschedule"
            }
        )
    ]
)
def test_unregister_schedule(local_manager, schedule_name, expected):
    removed_schedule = local_manager.unregister_schedule(schedule_name)


def test_list_schedules(local_manager):
    schedules = local_manager.list_schedules()
    
def test_register_trigger(local_manager):
    trigger = local_manager.register_trigger()

def test_unregister_trigger(local_manager):
    removed_trigger = local_manager.unregister_trigger()
    
def test_list_triggers(local_manager):
    triggers = local_manager.list_triggers()
