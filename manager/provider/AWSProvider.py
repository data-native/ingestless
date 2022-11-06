"""
AWS Backend Provider that implements the integration
with the AWS services. 


"""
import boto3
import logging
from manager.models import FunctionModel, TriggerModel, ScheduleModel
from typing import Optional, List, Dict
from botocore.client import BaseClient as BotoClient
from botocore import exceptions as BotoCoreExceptions

from manager.enums import Services
from manager.types import EventTargetItem
from manager.provider.abstract_provider import BackendProvider


class AWSProvider(BackendProvider):
    """
    AWS Backend provider implementation
    """
    def __init__(self, profile:str='') -> None:
        self.profile = None 
        self.session = boto3.Session(profile_name=profile) if profile !='' else boto3.Session()
        self._clients = {}
        # Maps the general Provider API to the AWS native services
        self.service_switch = {
            Services.Function : 'lambda',
            Services.ServiceBus : 'events',
            Services.StateMachine : 'stepfunctions',
        }
        super().__init_subclass__()

    def is_configured(self) -> bool:
        return self.session is not None

    def get_configuration(self):
        # Check if aws credentials are set
        credentials = self.session.get_credentials()
        return credentials
    
    def get_profiles(self) -> List:
        profiles = self.session.available_profiles
        return profiles
    
    def switch_profile(self, profile: str) -> None:
        profiles = self.get_profiles()
        if not profile in profiles:
            raise ValueError(f'Profile: {profile} not set. Available: {profiles}')
        self.session = boto3.Session(profile_name=profile) 

    def set_local_configuration(self):
        return super().set_local_configuration()
    
    def get_region(self) -> None:
        return super().get_region()

    # Client__________
    def get_client(self, service: Services) -> BotoClient:
        """Retrieves the correct native service for the framework service"""
        self._ensure_client(service)
        return self._clients[service]        

    def _initialize_client(self, service: Services) -> None:
        self._clients[service] = boto3.client(self.service_switch[service])

    def _ensure_client(self, service: Services) -> None: 
        if not service in self._clients:
            self._initialize_client(service)

    # Functions____________
    def list_functions(self) -> List[Dict]:
        functions = self.get_client(Services.Function).list_functions()
        return functions['Functions']
    
    def describe_function(self, name: str) -> Dict:
        function = self.get_client(Services.Function).describe_function(name)
        return function
    
    # EVENTS__________________-
    def describe_rule(self, name: str):
        """
        Retrieves details of a rule
        """
        response = self.get_client(Services.ServiceBus).describe_rule(name=name)
        # response = self._clients[Services.ServiceBus].describe_rule(name=name)

    def disable_rule(self, name:str):
        """
        Disables a rule
        """
        response = self._clients[Services.ServiceBus].disable_rule(name)
    
    def enable_rule(self, name:str):
        """
        Enables a given rule
        """
        response = self._clients[Services.ServiceBus].enable_rule(name)
    
    def list_rules_by_target(self, targetArn:str):
        """
        Lists the rules for the specified target.
        """
        # 
    def list_rules(self, prefix:str=''):
        """
        Lists all Bus rules.
        Can provide a prefix to filter the result set.
        """
        response = self._clients[Services.ServiceBus].list_rules(NamePrefix=prefix)
        return response
    
    def list_targets_by_rule(self, rule:str):
        """
        Lists all targets of the given rule:
        @rule: (str) Name of the rule to inspect
        """
        response = self._clients[Services.ServiceBus].list_targets_by_rule()
    
    def put_permissions(self, action: str, principal: str, statementId: str, condition: dict):
        """
        Puts a permission to the specified AWS account to put 
        events to your account. 
        """
        response = self._clients[Services.ServiceBus].put_permissions(Action=action, Principal=principal, StatementId=statementId, Condition=condition)
        return response
    
    def put_rule(self, rule: dict):
        """
        Add or update a given rule which is set active on default.
        """
        try:
            response = self.get_client(Services.ServiceBus).put_rule(**rule)
            return response['RuleArn'] 
        except BotoCoreExceptions.ClientError as client_e:
            logging.debug(f"event put_rule::ClientError: {client_e}")
            raise(client_e)

     
    def put_targets(self,
        rule: str,
        targets: List[EventTargetItem],
    ):
        """
        Add or update a given rule which is set active on default.
        """
        try:
            response = self.get_client(Services.ServiceBus).put_targets(
                Rule=rule,
                Targets=targets
                )
        except Exception as e:
            logging.debug(f"AWSProvider::put_targets: Error {e}")
            raise(e) 
    
    def put_target(self, 
        rule: str,
        type: Services,
        target
    ):
        """
        Supports the association of a rule with a specified Service type
        by retrieving the details and filling in the request body message.
        """
        response = None
        if type == Services.Function:
            # Fill lambda details
            # TODO: Use predefined Role to trigger the target lambda function
            function_target = EventTargetItem(
                Id=target['FunctionName'],
                Arn= target['FunctionArn']
            )
            response = self.get_client(Services.ServiceBus).put_targets(
                Rule=rule,
                Targets=[function_target.__dict__]
            )
        if type == Services.StateMachine:
            # Fill lambda details
            raise NotImplementedError
        return response

    
# class AzureProvider(BackendProvider):
    # pass

# class GCPProvider(BackendProvider):
    # pass

# class CloudNativeProvider(BackendProvider):
    # pass