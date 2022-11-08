import logging
import pickle
from typing import NamedTuple, List, Any, Dict
from pynamodb.models import MetaModel

from manager.enums import StatusCode, Errors
from manager.types import FunctionItem
from manager.models import FunctionModel, ScheduleModel, TriggerModel, Models
from manager.utils import dynamoutils

logger = logging.getLogger('root')
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
        self.models = {
            'Function': FunctionModel,
            'Trigger': TriggerModel
        
        }

    # FUNCTIONS_______________
    def read_function(self, function_hk:str):
        """
        Read a single function from the backend
        """
        function = FunctionModel.get(hash_key=function_hk)
        return dynamoutils.load_function_instance(function)

    def read_functions(self, stack: str='', details: bool = False):
        """
        Read the list of registered lambdas managed in the orchestration
        framework. 

        @stack: Limits the output of the list to the lambas from a given stack
        @details: Display details of the lambda functions or present a summarized list
        """
        functions = FunctionModel.scan()
        return [dynamoutils.load_function_instance(func) for func in functions] 
        # return DBResponse(functions, StatusCode.SUCCESS) 

    def write_function(self, function: FunctionModel) -> DBResponse:
        """
        Adds a management table entry and configures the appropriate 
        IAM integration.
        """
        logger.info(f"Registering FunctionModel object {function}")
        try:
            response = function.save()
        except:
            logger.exception("DB Write Error")
            return DBResponse(items={}, status=StatusCode.DB_WRITE_ERROR) 
        return DBResponse(items=response, status=StatusCode.SUCCESS) 
        # TODO: Define the table schema for the lambda management and create the insert data here

    def delete_function(self, function_name: str) -> DBResponse:
        """
        Removes a lambda from management in the orchestration service.
        Clears the metadata, and removes all triggers associated with the completion
        of this lambda in the orchestrator. 
        """
        function = FunctionModel.get(function_name)
        removed_function = function.delete()
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
        return dynamoutils.load_schedule_instance(schedule)

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
            function.update(actions=[
                FunctionModel.schedule.set(pickle.dumps(schedule)),
                FunctionModel.status.set("ENABLED")
                ])
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
