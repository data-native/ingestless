from dataclasses import dataclass

@dataclass
class ScheduleItem:
    "Class for passing Schedule definitions"
    name: str
    cron: str

@dataclass
class FunctionItem:
    name: str
    arn: str
    schedule: str

@dataclass
class TriggerItem:
    name: str
    