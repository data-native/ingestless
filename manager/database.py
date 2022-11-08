from enum import Enum
from pyclbr import Function
from typing import NamedTuple, List, Any, Dict
from pynamodb.models import MetaModel
import pickle


from manager.enums import StatusCode, Errors
from manager.types import FunctionItem
from manager.models import FunctionModel, ScheduleModel, TriggerModel, Models

class DBResponse(NamedTuple):
    items: Dict[str, Dict[str, Any]]
    status: StatusCode
class DatabaseHandler:
    """
    Manages the interaction with the data storage services available
    in the application. 

    Functionality
    -----------------
    * Register a model with the service and make it visible
    * Implement the internal API to 
    """

    def __init__(self):
        self._registered_lambdas: Dict[str, Dict[str, Any]] = {}
        self.models = {
            'Function': FunctionModel,
            'Trigger': TriggerModel
        
        }

    # FUNCTIONS_______________
    def write_function(self, function: FunctionItem):
        """
        Write a function to the database. 
        """
        raise NotImplementedError

    def read_function(self, function_hk:str):
        """
        Read a single function from the backend
        """
        function = FunctionModel.get(hash_key=function_hk)
        return function

    def read_functions(self, stack: str='', details: bool = False):
        """
        Read the list of registered lambdas managed in the orchestration
        framework. 

        @stack: Limits the output of the list to the lambas from a given stack
        @details: Display details of the lambda functions or present a summarized list
        """
        functions = FunctionModel.scan()
        return list(functions)
        # return DBResponse(functions, StatusCode.SUCCESS) 

    def write_functions(self, lambda_list: Dict[str, Dict[str, Any]]) -> DBResponse:
        """
        Registers management for a specified lambda.
        Adds a management table entry and configures the appropriate 
        IAM integration.
        """
        # TODO: Define the table schema for the lambda management and create the insert data here
        self._registered_lambdas.update(lambda_list)
        return DBResponse(lambda_list, StatusCode.SUCCESS)

    def unregister_function(self, function_name: str) -> DBResponse:
        """
        Removes a lambda from management in the orchestration service.
        Clears the metadata, and removes all triggers associated with the completion
        of this lambda in the orchestrator. 
        """
        removed_function = self._registered_lambdas.pop(function_name)
        return DBResponse(removed_function, StatusCode.SUCCESS)



    # SCHEDULES___________________
    def read_schedules(self) -> List[ScheduleModel]:
        """
        Retrieves the list of schedules 
        """
        schedules = ScheduleModel.scan(page_size=None)
        return list(schedules)
    
    def read_schedule(self, name: str) -> ScheduleModel:
        """Retrieves a schedule by name"""
        schedule = ScheduleModel.get(name)
        return schedule

    def set_schedule(self, target: MetaModel, target_id: str, schedule_id: str) -> StatusCode:
        """
        Associates a schedulable type with a schedule
        
        @target: FUNCTION, BATCH
        @target_id: Identifier set for the target instance type
        @schedule_id: Identifier for the target schedule
        """
        schedule = self.read_schedule(schedule_id)
        if target == Models.FUNCTION.value:
            function = self.read_function(target_id)
            function.update(actions=[FunctionModel.schedule.set(pickle.dumps(schedule))])
        else:
            raise ValueError(f"The selected type {target} is not schedulable")
        return StatusCode.SUCCESS
    
    def unset_schedule(self, target: MetaModel, target_id: str):
        """
        Nulls out the schedule on the specified target
        """
        if target == Models.FUNCTION:
            function = self.read_function(target_id)
            function.update(actions=[FunctionModel.schedule.set(None)]) 
