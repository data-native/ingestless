"""
AWS Backend Provider that implements the integration
with the AWS services. 


"""
import boto3
from manager.models import FunctionModel, TriggerModel, ScheduleModel
from typing import Optional, List, Dict
from manager.enums import Service
from manager.provider.abstract_provider import BackendProvider

class AWSProvider(BackendProvider):
    """
    AWS Backend provider implementation
    """
    def __init__(self, profile:str='') -> None:
        self.profile = None 
        self.session = boto3.Session(profile_name=profile) if profile !='' else boto3.Session()
        self.clients = {}
        # Maps the general Provider API to the AWS native services
        self.service_switch = {
            Service.Function : 'lambda',
            Service.ServiceBus : 'eventbridge',
            Service.StateMachine : 'stepfunctions',
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
    def get_client(self, service: Service):
        """Retrieves the correct native service for the framework service"""
        self._ensure_client(service)
        return self.clients[service]        

    def _initialize_client(self, service: Service) -> None:
        self.clients[service] = boto3.client(self.service_switch[service])

    def _ensure_client(self, service: Service): 
        if not service in self.clients:
            self._initialize_client(service)

    # Functions____________
    def list_functions(self) -> List[Dict]:
        functions = self.get_client(Service.Function).list_functions()
        return functions['Functions']
    
    # EVENTS__________________-
    def describe_rule(self, name: str):
        """
        Retrieves details of a rule
        """
        response = self.clients[Service.ServiceBus].describe_rule(name=name)

    def disable_rule(self, name:str):
        """
        Disables a rule
        """
        response = self.clients[Service.ServiceBus].disable_rule(name)
    
    def enable_rule(self, name:str):
        """
        Enables a given rule
        """
        response = self.clients[Service.ServiceBus].enable_rule(name)
    
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
        response = self.clients[Service.ServiceBus].list_rules(NamePrefix=prefix)
        return response
    
    def list_targets_by_rule(self, rule:str):
        """
        Lists all targets of the given rule:
        @rule: (str) Name of the rule to inspect
        """
        response = self.clients[Service.ServiceBus].list_targets_by_rule()
    
    def put_permissions(self, action: str, principal: str, statementId: str, condition: dict):
        """
        Puts a permission to the specified AWS account to put 
        events to your account. 
        """
        response = self.clients[Service.ServiceBus].put_permissions(Action=action, Principal=principal, StatementId=statementId, Condition=condition)
        return response
    
    def put_rule(self):
        """
        Add or update a given rule which is set active on default.
        """
        raise NotImplementedError

    def put_targets(self):
        """
        Add or update a given rule which is set active on default.
        """
        raise NotImplementedError

# class AzureProvider(BackendProvider):
    # pass

# class GCPProvider(BackendProvider):
    # pass

# class CloudNativeProvider(BackendProvider):
    # pass