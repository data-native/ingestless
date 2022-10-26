from manager.database import DatabaseHandler
from typing import List, Dict, Any, Optional

class Manager:
    def __init__(self):
        self._db_handler = DatabaseHandler()
        self._registered_lambdas = []

    def register_function(self, function_name: str, body: Dict[str, Any]) -> None:
        """
        Register a lambda function with the orchestrator.
        
        """ 
        raise NotImplementedError

    def unregister_function(self, function_name: str) -> None:
        """
        Removes a lambda function from orchestrator management.
        """
        raise NotImplementedError

    def list_functions(self, stack: str='') -> Optional[List[Dict]]:
        """
        Lists the available lambda functions in a given account. 
        Optionally filter by deployment stack, accountId.

        @stack: String naming a specific CloudFormation Stack to list
        @region: Select a region to list lambdas in
        """
        raise NotImplementedError

    def register_schedule(self):
        """
        Register an execution schedule to associate it with any
        function as trigger.
        """
        raise NotImplementedError
    
    def unregister_schedule(self, schedule_name: str):
        """
        Removes a schedule from the system.
        """
        raise NotImplementedError
    
    def list_schedules(self):
        """
        Lists all defined schedules within the orchestrator.
        """
        raise NotImplementedError
    
    def register_trigger(self):
        """
        Register a trigger for a function from a connected
        service. 

        Can be any type of trigger supported by lambda
        """
        raise NotImplementedError
    
    def unregister_trigger(self):
        """
        Removes a trigger from the given function.
        """
        raise NotImplementedError

    def list_triggers(self):
        """
        List the registered triggers within the orchestrator.
        """
        raise NotImplementedError