from typing import List, Dict
from dataclasses import dataclass

@dataclass
class FunctionItem:
    """
    Defines the attributes required to be set for a function
    to be registered in the system. 
    """
    name: str
    attributes: dict


@dataclass
class ScheduleItem:
    """
    Defines the attributes required to be set for a schedule
    to be registered in the system. 
    """
    name: str
    cron: str

@dataclass
class TriggerItem:
    """
    Defines the attributes required to be set for a trigger
    to be registered in the system. 
    """
    name: str
    source: str

# Request items used in Provider Class
@dataclass
class EventTargetItem:
    """
    A request item send definition used in the
    put_targets call to the AWS Backend provider
    """
    Id: str
    Arn: str
    # RoleArn: str = ''
    # Input: str = ''
    # InputPath: str = ''
    # InputTransformer: = {}

@dataclass
class AWSRuleItem:
    """
    An event rule instance required to schedule
    execution of targets on AWS EventBus
    """
    Name : str
    ScheduleExpression: str
    State: str = 'DISABLED'
    Description: str = ''