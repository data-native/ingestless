import logging
import pickle
from configparser import ConfigParser
from sre_constants import SUCCESS
from manager.enums import StatusCode, RequestModels
from manager.database import DatabaseHandler
from typing import Iterator, List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from manager.enums import Provider
from manager.provider.AWSProvider import AWSProvider
from manager.provider.abstract_provider import BackendProvider
from manager.models import TriggerModel, ScheduleModel, FunctionModel
from manager.config import ConfigManager


class Models:
    FUNCTION = FunctionModel
    SCHEDULE = ScheduleModel
    TRIGGER = TriggerModel

class Manager:
    """
    Provides the general interface to the application logic.
    
    * CRUD API for all supported types.
    """

    def __init__(self):
        self.models =  Models
        self.requests = RequestModels
        self._registered_lambdas = {} 
        self._config_manager = ConfigManager()
        self._backend = DatabaseHandler() 
        self._provider = self._init_provider()

    # INITIALITAION___________________
    def _init_backend(self):
        """Initializes the backend application"""
    
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
        function: Models.FUNCTION,
    ) -> StatusCode:
        """
        Register a lambda function with the orchestrator.
        
        """ 
        try:
            logging.info(f"Registering FunctionModel object {function}")
            function.save()
            self._registered_lambdas[function.name] = function
        except Exception as e:
            raise(e)
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

    def list_functions(self, stack: str='') -> Optional[List[dict]]:
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
    
    def list_registered_functions(self, stack:str='') -> List[FunctionModel]:
        """
        List the registered functions in the manager.
        Optionally limit the results to a given application.
        #TODO: Add support for applications within the manager later

        @app: Application name for which to list the registered functions
        """
        try:
            registered_functions = self._backend.read_functions(stack)
            return list(registered_functions)
        except Exception as e:
            raise(e)

    # SCHEDULE_________________________
    def register_schedule(self, schedule: Models.SCHEDULE) -> StatusCode:
        """
        Register an execution schedule to associate it with any
        function as trigger.
        """
        try:
            schedule.save()
        except Exception as e:
            #TODO: Handle exception 
            logging.exception(e)
            return  StatusCode.DB_WRITE_ERROR
        return StatusCode.SUCCESS
    
    def unregister_schedule(self, schedule_name: str ):
        """
        Removes a schedule from the system.
        """
        try:
            schedule = ScheduleModel.get(schedule_name)
            schedule.delete()
            logging.debug("Removed")
        except Exception as e:
            raise(e)                
            #TODO: Log exception
            StatusCode.DB_WRITE_ERROR
        StatusCode.SUCCESS
    
    def list_schedules(self):
        """
        Lists all defined schedules within the orchestrator.
        """
        try:
            schedules = ScheduleModel.scan()
            return list(schedules)
        except Exception as e:
            #TODO: Log exception
            raise e 
    
    def schedule_function(self, schedule: ScheduleModel, function_hk: str, function_sk: str = '') -> StatusCode:
        """
        Applies a registered schedule to the function
        """
        try:
            function = FunctionModel.get(function_hk)
            function.update(actions=[self.models.FUNCTION.schedule.set(pickle.dumps(schedule))])
            return StatusCode.SUCCESS 
        except Exception as e:
            logging.exception("Exception updating function with schedule", e)
            return StatusCode.DB_WRITE_ERROR


    # TRIGGER_________________________
    def register_trigger(self, trigger: Models.TRIGGER) -> StatusCode:
        """
        Register a trigger for a function from a connected
        service. 

        Can be any type of trigger supported by lambda
        """
        try:
            trigger.save()
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

    def list_triggers(self) -> Iterator[Models.TRIGGER]:
        """
        List the registered triggers within the orchestrator.
        """
        try:
            triggers = TriggerModel.scan()
            yield triggers.next()
        except Exception as e:
            #TODO: Log exception
            raise e 