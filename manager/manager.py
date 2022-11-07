import logging
import pickle
from configparser import ConfigParser
from sre_constants import SUCCESS
from manager.enums import StatusCode, RequestModels
from manager.database import DatabaseHandler
from typing import Iterator, List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass

from manager.enums import Provider
from manager.provider.AWS.AWSProvider import AWSProvider
from manager.provider.abstract_provider import BackendProvider
from manager.models import TriggerModel, ScheduleModel, FunctionModel
from manager.config import ConfigManager

# Import custom logger 
logger = logging.getLogger('root')

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
            logger.info(f"Registering FunctionModel object {function}")
            function.save()
            self._registered_lambdas[function.name] = function
        except Exception as e:
            raise(e)
            #TODO: Log exception
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

    def describe_function(self, name:str) -> dict:
        """
        Describe a specific function
        """
        try:
            function = self._provider.describe_function(name)
            return function
        except Exception as e:
            raise(e)

    # SCHEDULE_________________________
    def register_schedule(self, schedule: Models.SCHEDULE) -> StatusCode:
        """
        Register an execution schedule to associate it with any
        function as trigger.
        """
        # Ensure all elements are pickled
        if not isinstance(schedule.cron, bytes):
            schedule.cron = pickle.dumps(schedule.cron)
        try:
            schedule.save()
            logger.debug(f'Registered Schedule: {schedule.name}')
        except Exception as e:
            #TODO: Handle exception 
            logger.exception(e)
            return  StatusCode.DB_WRITE_ERROR
        return StatusCode.SUCCESS
    
    def unregister_schedule(self, schedule_name: str ):
        """
        Removes a schedule from the system.
        """
        try:
            schedule = ScheduleModel.get(schedule_name)
            schedule.delete()
            logger.debug(f"Removed Schedule {schedule.name}")
        except Exception as e:
            raise(e)                
            #TODO: Log exception
            StatusCode.DB_WRITE_ERROR
        StatusCode.SUCCESS
    
    def list_schedules(self) -> List[ScheduleModel]:
        """
        Lists all defined schedules within the orchestrator.
        """
        try:
            schedules = self._backend.read_schedules()
            return schedules
        except Exception as e:
            #TODO: Log exception
            raise e 
    
    def describe_schedule(self, schedule_name: str) -> ScheduleModel:
        """Retrieves the model for the schedule by name"""
        try:
            schedule = self._backend.read_schedule(name=schedule_name)
            return schedule 
        except Exception as e:
            raise(e)

    def schedule_function(self, schedule: Optional[ScheduleModel], function_hk: str, function_sk: str = '') -> StatusCode:
        """
        Applies a registered schedule to the function.
        
        Allows to set the schedule to None to effectively remove the schedule
        from the function.
        """
        from manager.types import AWSRuleItem
        from manager.provider.AWS import utils as AWSUtils 
        try:
            function = FunctionModel.get(function_hk)
            # Update schedule information on function instance entry
            function.update(actions=[self.models.FUNCTION.schedule.set(pickle.dumps(schedule))])
            if schedule:
                # Update the schedule instance on the backend
                schedule.update(actions=[self.models.SCHEDULE.associated.set(self.models.SCHEDULE.associated.append([function_hk]))])
            
                #TODO: Simplify logic with passing dict and pickle loading 
                rule = AWSRuleItem(
                   Name=schedule.name,
                   ScheduleExpression=AWSUtils.compile_schedule_expression(schedule.cron),
                   State='ENABLED'
                )
                self._provider.put_rule(rule.__dict__)
                logger.debug(f"Scheduled function {function_hk} with schedule {rule.ScheduleExpression}")
            return StatusCode.SUCCESS 
        except Exception as e:
            logger.exception("Exception updating function with schedule", e)
            return StatusCode.DB_WRITE_ERROR
    
    def unschedule_function(self, name: str) -> StatusCode:
        """
        Clears a schedule on the given schedule
        """
        try:
            self.schedule_function(None, name)
            return StatusCode.SUCCESS
        except Exception as e:
            logger.exception(f"Removing schedule from function {name}")
            return StatusCode.DB_WRITE_ERROR

    def unregister_function(self, name:  str) -> StatusCode:
        """
        Removes a function from registration.
        All elements associated with the function get also deassigned, or removed
        if this was the only association they held and they are not stand-alone.
        """
        try:
            function = self._backend.read_function(name) 
        except:
            pass 
        try:
            # Check for all elements associated with this function
            self.unschedule_function(function.name)
            # Clean up all associations
            #TODO: Remove other assocations with the function
            # If successfully, remove the function

            self._backend.unregister_function(name)
            return StatusCode.SUCCESS
        except Exception as e:
            logger.exception(f"Unregistering function {function.name} raised")
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