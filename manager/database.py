from typing import NamedTuple, List, Any, Dict
from manager.enums import StatusCode, Errors

class DBResponse(NamedTuple):
    items: Dict[str, Dict[str, Any]]
    status: StatusCode


class DatabaseHandler:

    def __init__(self):
        self._registered_lambdas: Dict[str, Dict[str, Any]] = {}

    def read_registered_lambdas(self, stack: str='', details: bool = False):
        """
        Read the list of registered lambdas managed in the orchestration
        framework. 

        @stack: Limits the output of the list to the lambas from a given stack
        @details: Display details of the lambda functions or present a summarized list
        """

        if details:
            # TODO: Generate the full response object array
            return DBResponse({
                'function1': {'name': 'function 1', },
                'function2': {'name': 'function 2', },
            } , StatusCode.SUCCESS)
        else:
            # TODO: Generate summarized list
            return [
                {'name': 'function1'}
            ]

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
