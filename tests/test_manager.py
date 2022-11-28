import json
from typing import Iterable
import pytest

from random import randint
from cron_converter import Cron
from typer.testing import CliRunner

from enums import StatusCode
from manager.database import DatabaseHandler
from manager.models import FunctionModel, ScheduleModel, TriggerModel
from manager.types import ScheduleItem
from manager.manager import Manager
from restmap.executor.AWS.AWSProvider import AWSExecutor


runner = CliRunner()

@pytest.fixture
def local_db():
    #TODO: Create connection to local DynamoDB instance
    #TODO: Initialize the local db with table schema
    #TODO: Place a starting set of data in local db
    return DatabaseHandler() 

@pytest.fixture(autouse=True)
def local_manager(local_db):
    return Manager() 

@pytest.fixture()
def function(local_manager: Manager):
    functions = local_manager.list_functions()
    function = functions[0]
    function = local_manager.models.FUNCTION(
            name=function['FunctionName'],
            resourceId=function['FunctionArn'],
            attributes = function,
            schedule = None,
            status = None,
        )
    return function

@pytest.fixture()
def registered_function(local_manager: Manager) -> FunctionModel:
    functions = local_manager.list_functions()
    function = functions[randint(0, len(functions)-1)]
    function = local_manager.models.FUNCTION(
            name=function['FunctionName'],
            resourceId=function['FunctionArn'],
            attributes = function,
            schedule = None,
            status = None,
        )
    status = local_manager.register_function(function)

    return function

@pytest.fixture()
def schedule(local_manager: Manager):
    cron = Cron('* 2 * * *', {})
    schedule = local_manager.models.SCHEDULE('testschedule', cron=cron)
    local_manager.register_schedule(schedule)
    return schedule

#TODO: Add a scheduled_function fixture
@pytest.fixture()
def scheduled_function(local_manager: Manager, schedule, registered_function: FunctionModel):
    local_manager.schedule_function(schedule.name, registered_function.name)
    return registered_function


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


class TestInitialization:

    def test_init_backend_provider(local_manager: Manager):
        manager = Manager('AWS')
        assert isinstance(manager, AWSExecutor)
        

# FUNCTIONS_________________
class TestFunctionManager:
    
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
    def test_register_functions(self, function_name, body, expected):
        raise NotImplementedError
        # status = self.manager.register_function(function_name, body)
        # assert isinstance(status, dict) 
        # assert isinstance(status["status"], StatusCode)

    def test_register_function(self, local_manager: Manager, function: FunctionModel):
        local_manager.register_function(function)
        assert function.name in local_manager._registered_functions
        # Cleanup
        local_manager.unregister_function(function.name)


    def test_list_functions(self, local_manager: Manager):
        functions = local_manager.list_functions()
        assert isinstance(functions, Iterable)
        assert isinstance(functions[0], dict)

    def test_list_registered_functions(self, local_manager: Manager):
        #TODO: Extend to create temporary tests in temp local db
        # local_manager.register_function(local_manager.models.FUNCTION("test", ))
        functions = local_manager.list_registered_functions() 
        assert isinstance(functions, list)
        assert all([isinstance(f, FunctionModel) for f in functions])

    def test_schedule_function(self, local_manager: Manager, schedule: ScheduleModel, registered_function: FunctionModel):
        """
        Ensure the schedule is stored on the function model, 
        is registered in the backend provider and is deployed by default
        """
        # Apply schedule
        schedule_status = local_manager.schedule_function(schedule.name, function_hk=registered_function.name)
        assert schedule_status == StatusCode.SUCCESS
        updated_function = local_manager.describe_function(registered_function.name)
        assert isinstance(updated_function['schedule'], ScheduleModel)
        assert updated_function['schedule'].name == schedule.name, ""
        assert updated_function['status'] == 'ENABLED', "Schedule set must be set to ENABLED"


    def test_unschedule_function(self, local_manager: Manager, schedule: ScheduleModel, registered_function: FunctionModel):
        """
        Ensure the schedule can be reset to None on the 
        chosen function.
        """
        from enums import Services
        # Remove the schedule from the function
        response = local_manager.unschedule_function(registered_function.name)
        assert response.SUCCESS, "Function must correctly complete with StatusCode.SUCCESS"
        rules = local_manager._provider.list_rules_by_target(
            type=Services.Function,
            target=registered_function.name)
        rule_dict = rules['RuleNames']
        #TODO: Check that the function model no longer has a schedule associated
        assert schedule.name not in rule_dict, "Schedule must be removed from the event routing rules for the function"
        function_names = [fun['FunctionName'] for fun in local_manager.list_functions()]
        assert registered_function.name in function_names, "Unscheduled function must still exist as a function"
        registered_function_names = [fun.name for fun in local_manager.list_registered_functions()]
        assert registered_function.name in registered_function_names, "Unscheduled function must still be registered in the system"


    def test_unregister_function(self, local_manager: Manager, registered_function: FunctionModel):
        """
        Ensure the function is properly removed with alle
        dependencies and associations cleaned up
        """
        response = local_manager.unregister_function(registered_function.name)
        assert response.SUCCESS, "Function 'unregister_function' must complete correctly with StatusCode.SUCCESS"
        functions = local_manager.list_functions()
        assert registered_function.name not in functions, "Function should be deleted from the database table"
        assert registered_function.name not in local_manager._registered_functions, "Function should be removed from manager registration state"


    def test_describe_function(self, local_manager: Manager, registered_function: FunctionModel):
        """
        Ensure a function description unified from backend provider
        details and orchestrator state specifics is returned
        """
        # Function call
        response = local_manager.describe_function(registered_function.name)
        assert isinstance(response, dict)
        assert 'attributes' in response, "Must contain the 'attributes' dict containing the function parameters from the backend"
        assert 'resourceId' in response, "Must contain a resourceId parameter by default"

    # HELPERS________________________
    def test_list_options(self, local_manager: Manager):
        raise NotImplementedError


# SCHEDULES _______________________
class TestScheduleManager:
    
    def test_register_schedule(self, local_manager: Manager):
        schedule = local_manager.models.SCHEDULE('test_schedule', cron=Cron('* * * * *'))
        local_manager.register_schedule(schedule)

    def test_unregister_schedule(self, local_manager: Manager):
        # Setup
        schedule = local_manager.models.SCHEDULE('test_schedule', cron=Cron('* * * * *'))
        local_manager.register_schedule(schedule)
        # Function call
        removed_schedule = local_manager.unregister_schedule('test_schedule')

    def test_list_schedules(self, local_manager: Manager):
        schedules = local_manager.list_schedules()

    def test_describe_schedule(self, local_manager: Manager, schedule: ScheduleModel, scheduled_function: FunctionModel):
        """
        Ensure all details about the schedule are queryable from the CLI
        """
        schedule = local_manager.describe_schedule(schedule_name=schedule.name)
        assert schedule

    # TRIGGERS_______________________
    def test_register_trigger(self, local_manager: Manager):
        raise NotImplementedError
        trigger = self.manager.register_trigger()

    def test_unregister_trigger(self, local_manager: Manager):
        raise NotImplementedError
        removed_trigger = self.manager.unregister_trigger()
        
    def test_list_triggers(self, local_manager: Manager):
        raise NotImplementedError
        triggers = self.manager.list_triggers()
