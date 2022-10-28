from configparser import ConfigParser
from manager.enums import StatusCode
from manager.database import DatabaseHandler
from typing import Iterator, List, Dict, Any, Optional

from manager.enums import Provider
from manager.provider.AWSProvider import AWSProvider
from manager.provider.abstract_provider import BackendProvider
from manager.types import FunctionItem, TriggerItem, ScheduleItem
from manager.models import ScheduleModel, TriggerModel, FunctionModel
from manager.config import ConfigManager

class Manager:

    def __init__(self):
        self._registered_lambdas = []
        self._config_manager = ConfigManager()
        self._provider = self._init_provider()

    # INITIALITAION___________________
    def _init_provider(self):
        """Initializes the selected provider"""
        # Read configuration for provider
        try:
            provider = self._config_manager.provider()
        except Exception:
            raise ValueError(f"Configuration Parameter for provider not correctly set")
        # Select the associated Provider
        provider_switch = {
            Provider.AWS : AWSProvider,
        }
        return provider_switch[provider]()

    # FUNCTION_________________________
    def register_function(self,
        function: FunctionItem,
    ) -> StatusCode:
        """
        Register a lambda function with the orchestrator.
        
        """ 
        try:
            function_item = FunctionModel(function)
            function_item.save()
        except:
            #TODO: Log exception
            StatusCode.DB_WRITE_ERROR
        return StatusCode.SUCCESS

    def unregister_function(self, function_name: str) -> StatusCode:
        """
        Removes a lambda function from orchestrator management.
        """
        try:
            FunctionModel.name.delete(function_name)
        except:
            StatusCode.DB_WRITE_ERROR
        return StatusCode.SUCCESS

    def list_functions(self, stack: str=''):
        """
        Lists the available lambda functions in a given account. 
        Optionally filter by deployment stack, accountId.

        @stack: String naming a specific CloudFormation Stack to list
        @region: Select a region to list lambdas in
        """
        try:
            functions = self._provider.list_functions()
            return functions
        except Exception as e:
            #TODO: Log exception
            raise(e) 

    # SCHEDULE_________________________
    def register_schedule(self, schedule: ScheduleItem) -> StatusCode:
        """
        Register an execution schedule to associate it with any
        function as trigger.
        """
        try:
            schedule_item = ScheduleModel(schedule)
            schedule_item.save()
        except:
            #TODO: Log exception
            return StatusCode.DB_WRITE_ERROR
        return StatusCode.SUCCESS
    
    def unregister_schedule(self, schedule_name: str ):
        """
        Removes a schedule from the system.
        """
        try:
            ScheduleModel.name.delete(schedule_name)
        except:
            #TODO: Log exception
            StatusCode.DB_WRITE_ERROR
        StatusCode.SUCCESS
    
    def list_schedules(self):
        """
        Lists all defined schedules within the orchestrator.
        """
        try:
            schedules = ScheduleModel.scan()
            yield schedules.next()
        except Exception as e:
            #TODO: Log exception
            raise e 

    # TRIGGER_________________________
    def register_trigger(self, trigger: TriggerItem) -> StatusCode:
        """
        Register a trigger for a function from a connected
        service. 

        Can be any type of trigger supported by lambda
        """
        try:
            trigger_item = TriggerModel(trigger)
            trigger_item.save()
        except:
            #TODO: Log exception
            return StatusCode.DB_WRITE_ERROR
        return StatusCode.SUCCESS
    
    def unregister_trigger(self, trigger_name: str):
        """
        Removes a trigger from the given function.
        """
        try:
            TriggerModel.name.delete(trigger_name)
        except:
            #TODO: Log exception
           return StatusCode.DB_WRITE_ERROR 
        return StatusCode.SUCCESS

    def list_triggers(self) -> Iterator[TriggerModel]:
        """
        List the registered triggers within the orchestrator.
        """
        try:
            triggers = TriggerModel.scan()
            yield triggers.next()
        except Exception as e:
            #TODO: Log exception
            raise e 