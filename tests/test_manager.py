import json
import pickle
from typing import Iterable
import pytest

from cron_converter import Cron
from typer.testing import CliRunner

from manager.database import DatabaseHandler
from manager.enums import StatusCode
from manager.types import ScheduleItem
from manager.manager import Manager

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

    def test_register_function(self, local_manager: Manager):
        functions = local_manager.list_functions()
        function = functions[0]
        local_manager.register_function(local_manager.models.FUNCTION(
            function['FunctionName'],
            resourceId=function['FunctionArn'],
            attributes=function
        ))
        assert function['FunctionName'] in local_manager._registered_functions
        # Cleanup
        local_manager.unregister_function(function['FunctionName'])


    def test_list_functions(self, local_manager: Manager):
        functions = local_manager.list_functions()
        assert isinstance(functions, Iterable)
        assert isinstance(functions[0], dict)

    def test_list_registered_functions(self, local_manager: Manager):
        #TODO: Extend to create temporary tests in temp local db
        # local_manager.register_function(local_manager.models.FUNCTION("test", ))
        functions = local_manager.list_registered_functions() 

        assert isinstance(functions, list)
        for f in functions:
            assert all([k in f._get_keys() for k in ['name', 'attributes', 'schedule']])

    def test_schedule_function(self, local_manager: Manager):
        """
        Ensure the schedule is stored on the function model, 
        is registered in the backend provider and is deployed by default
        """
        # Preparation
        function = local_manager.models.FUNCTION('test', attributes={})
        local_manager.register_function(function)
        cron = Cron('* 2 * * *', {})
        schedule = local_manager.models.SCHEDULE('testschedule', cron=cron)
        local_manager.register_schedule(schedule)
        # Apply schedule
        schedule_status = local_manager.schedule_function(schedule.name, function_hk='test')
        assert schedule_status == StatusCode.SUCCESS

    def test_unschedule_function(self, local_manager: Manager):
        """
        Ensure the schedule can be reset to None on the 
        chosen function.
        """
        from manager.enums import Services
        # Set the function
        function = local_manager.models.FUNCTION('test', attributes={})
        local_manager.register_function(function)
        cron = Cron('* 2 * * *', {})
        schedule = local_manager.models.SCHEDULE('testschedule', cron=cron)
        local_manager.register_schedule(schedule)
        local_manager.schedule_function(schedule.name, function.name)
        # Remove the function
        response = local_manager.unschedule_function(function.name)
        assert response.SUCCESS
        assert local_manager._provider.list_rules_by_target(
            type=Services.Function,
            target=function.name)
    def test_unregister_function(self, local_manager: Manager):
        """
        Ensure the function is properly removed with all
        dependencies and associations cleaned up
        """
        # Prep
        schedule = local_manager.models.SCHEDULE(
            name='testschedule',
            cron = Cron('3 * * * *')
        )
        function = local_manager.models.FUNCTION('empheral', 
        attributes={},
        schedule = pickle.dumps(schedule)
        )
        local_manager.register_function(function)
        # Function call
        response = local_manager.unregister_function(function.name)
        assert response

    def test_describe_function(self, local_manager: Manager):
        """
        Ensure a function description unified from backend provider
        details and orchestrator state specifics is returned
        """
        # Setup
        functions = local_manager.list_functions()
        function = functions[0] 
        # Function call
        response = local_manager.describe_function(function['FunctionName'])
        assert isinstance(response, dict)

    # 

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

    def test_describe_schedule(self, local_manager: Manager):
        """
        Ensure all details about the schedule are queryable from the CLI
        """
        # Create a schedule
        schedule = local_manager.models.SCHEDULE('test_schedule', cron='5 * * * *')
        local_manager.register_schedule(schedule)
        schedule = local_manager.describe_schedule(schedule_name=schedule.name)

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
