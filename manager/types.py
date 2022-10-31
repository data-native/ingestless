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