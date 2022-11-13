import logging
import pickle
from manager.enums import StatusCode, RequestModels
from manager.database import DatabaseHandler
from typing import Iterator, List, Dict, Any, Optional, Tuple, Union

from manager.enums import Provider
from manager.provider.AWS.AWSProvider import AWSProvider
from manager.models import TriggerModel, ScheduleModel, FunctionModel
from manager.config import ConfigManager
from manager.utils import dynamoutils as functionUtils

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
        self._registered_functions = {} 
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
        Register a serverless function with the orchestrator.

        #TODO: Store only the parameters that don't change in the database, or make sure to find a way to keep them current enough 
        #TODO: Ensure that deployed changes to the functions trigger an update on the metadata in the orchestrator (Maybe implement in Make file and force the use)
        """ 
        try:
            self._registered_functions[function.name] = function
            self._backend.write_function(function)
        except Exception as e:
            raise(e)
            #TODO: Log exception
            StatusCode.DB_WRITE_ERROR
        return StatusCode.SUCCESS

    def unregister_function(self, name:  str) -> StatusCode:
        """
        Removes a function from registration.
        All elements associated with the function get also deassigned, or removed
        if this was the only association they held and they are not stand-alone.
        """
        function = self._backend.read_function(name) 
        try:
            # Check for all elements associated with this function
            self.unschedule_function(function.name)
            # Clean up all associations
            #TODO: Remove other assocations with the function
            # If successfully, remove the function

            self._backend.delete_function(name)
            self._registered_functions.pop(name)
            return StatusCode.SUCCESS
        except Exception as e:
            logger.exception(f"Unregistering function {function.name} raised")
            return StatusCode.DB_WRITE_ERROR


    def list_functions(self, stack: str='') -> List[dict]:
        """
        Lists the available lambda functions in a given account. 
        Optionally filter by deployment stack, accountId.

        @stack: String naming a specific CloudFormation Stack to list
        @region: Select a region to list lambdas in
        """
        try:
            #TODO: Implement limit on stack
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

    def describe_function(self, 
        name:str,
        params: List[str] = [],
        ) -> dict:
        """
        Describe a specific function
        @params: The list of strings identifying the attributes to describe 
        """
        try:
            function_provider = self._provider.read_function(name)
            function_meta = self._backend.read_function(name)
            if function_meta.schedule:
                function_meta.schedule = function_meta.schedule
            function_meta = function_meta.__dict__['attribute_values']

            #Subset the entries to the relevant fields
            if params:
                function_meta = {key: item for key, item in function_meta.items() if key in params}
            function_provider = function_provider['Configuration']
            function_meta['attributes'] = function_meta['attributes'] | function_provider
            return function_meta 

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

    def schedule_function(self, schedule_id: str, function_hk: str) -> StatusCode:
        """
        Applies a registered schedule to the function.
        #TODO: Generalize for multiple providers by moving out the provider logic into provider class
        """
        from cron_converter import Cron
        from manager.types import AWSRuleItem

        from manager.provider.AWS import utils as AWSUtils 
        try:
            # Update schedule information on function instance entry
            schedule = self._backend.read_schedule(schedule_id)
            self._backend.set_schedule(target=self.models.FUNCTION, schedule_id=schedule_id, target_id=function_hk)
            # Update the schedule instance on the backend
            # if not isinstance(schedule.cron, Cron):
                # schedule.cron = pickle.loads(schedule.cron)
            
            #TODO: Simplify logic with passing dict and pickle loading 
            rule = AWSRuleItem(
               Name=schedule_id,
               ScheduleExpression=AWSUtils.compile_schedule_expression(schedule.cron),
               State='ENABLED'
            )
            self._provider.put_rule(rule.__dict__)
            logger.debug(f"Scheduled function {function_hk} with schedule {rule.ScheduleExpression}")
            return StatusCode.SUCCESS 
        except Exception as e:
            logger.exception("Exception updating function with schedule", e)
            return StatusCode.DB_WRITE_ERROR
    
    def unschedule_function(self, function: Union[str, FunctionModel]) -> StatusCode:
        """
        Removes the schedule from the given function 
        """
        function_model: FunctionModel = function if isinstance(function, FunctionModel) else self._backend.read_function(function)
        if not function_model.schedule:
            return StatusCode.SUCCESS
        try:
            rule_name = function_model.schedule.name

            # Remove rule
            self._backend.unset_schedule(target=self.models.FUNCTION, target_id=function_model.name)
            response = self._provider.remove_event_targets(
                rule=function_model.schedule.name,
                type=self.models.FUNCTION,
                targets=function_model.name
            )
            # Check that there are still functions asscoiated otherwise disable the rule
            active_targets = self._provider.list_targets_by_rule(rule_name)
            if not active_targets:
                self._provider.disable_rule(rule_name)
            return StatusCode.SUCCESS
        except Exception as e:
            logger.exception(f"Removing schedule from function {function_model}")
            return StatusCode.DB_WRITE_ERROR

    def toggle_event_status(self, name: str) -> StatusCode:
        """
        Toggles the event status, pausing or starting the schedule trigger for
        a given function.
        """ 
        try:
            function = self._backend.read_function(name)
            self._backend.toggle_schedule(target= self.models.FUNCTION, target_id=function.schedule.name)
        except Exception as e:
            raise(e)
        return StatusCode.SUCCESS
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