from manager.database import DatabaseHandler
from typing import List, Dict, Any, Optional

from manager.types import Schedule, Trigger, Function

    def __init__(self):
        self._db = DatabaseHandler()
        self._registered_lambdas = []

    # FUNCTION_________________________
    def register_function(self, function_name: str, body: Dict[str, Any]) -> None:
        """
        Register a lambda function with the orchestrator.
        
        """ 
        try:

        except:
            pass
        raise NotImplementedError

    def unregister_function(self, function_name: str) -> None:
        """
        Removes a lambda function from orchestrator management.
        """
        try:

        except:
            pass
        raise NotImplementedError

    def list_functions(self, stack: str='') -> Optional[List[Dict]]:
        """
        Lists the available lambda functions in a given account. 
        Optionally filter by deployment stack, accountId.

        @stack: String naming a specific CloudFormation Stack to list
        @region: Select a region to list lambdas in
        """
        try:

        except:
            pass
        raise NotImplementedError

    # SCHEDULE_________________________
    def register_schedule(self, schedule: Schedule):
        """
        Register an execution schedule to associate it with any
        function as trigger.
        """
        try:

        except:
            pass
        raise NotImplementedError
    
    def unregister_schedule(self, schedule_name: str ):
        """
        Removes a schedule from the system.
        """
        try:

        except:
            pass
        raise NotImplementedError
    
    def list_schedules(self):
        """
        Lists all defined schedules within the orchestrator.
        """
        try:

        except:
            pass
        raise NotImplementedError
    
    # TRIGGER_________________________
    def register_trigger(self):
        """
        Register a trigger for a function from a connected
        service. 

        Can be any type of trigger supported by lambda
        """
        try:

        except:
            pass
        raise NotImplementedError
    
    def unregister_trigger(self):
        """
        Removes a trigger from the given function.
        """
        try:

        except:
            pass
        raise NotImplementedError

    def list_triggers(self):
        """
        List the registered triggers within the orchestrator.
        """
        try:

        except:
            pass
        raise NotImplementedError