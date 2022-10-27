from dataclasses import dataclass

@dataclass
class Schedule:
    "Class for passing Schedule definitions"
    name: str
    cron: str

@dataclass
class Function:
    name: str
    arn: str

@dataclass
class Trigger:
    name: str
    