from enum import Enum
from pyclbr import Function
from typing import NamedTuple, List, Any, Dict
from manager.enums import StatusCode, Errors
from manager.types import FunctionItem
from manager.models import FunctionModel, ScheduleModel, TriggerModel

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

    def write_function(self, function: FunctionItem):
        """
        Write a function to the database. 
        """

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

    def write_lambdas(self, lambda_list: Dict[str, Dict[str, Any]]) -> DBResponse:
        """
        Registers management for a specified lambda.
        Adds a management table entry and configures the appropriate 
        IAM integration.
        """
        # TODO: Define the table schema for the lambda management and create the insert data here
        self._registered_lambdas.update(lambda_list)
        return DBResponse(lambda_list, StatusCode.SUCCESS)

    def unregister_lambda(self, function_name: str) -> DBResponse:
        """
        Removes a lambda from management in the orchestration service.
        Clears the metadata, and removes all triggers associated with the completion
        of this lambda in the orchestrator. 
        """
        removed_function = self._registered_lambdas.pop(function_name)
        return DBResponse(removed_function, StatusCode.SUCCESS)
