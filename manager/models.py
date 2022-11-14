from enum import Enum
from platform import system
import configparser
from datetime import datetime, timezone

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BinaryAttribute, BooleanAttribute, UTCDateTimeAttribute, JSONAttribute, ListAttribute 

parser = configparser.ConfigParser()
parser.read('./manager/config.ini')

env = 'dev' if system().lower() == 'darwin' else 'prod'

HOST = parser[env]['dynamodb_host']

FUNCTION_TABLE_NAME = parser['DEFAULT']['function_table_name']
SCHEDULE_TABLE_NAME = parser['DEFAULT']['schedule_table_name']
TRIGGER_TABLE_NAME = parser['DEFAULT']['trigger_table_name']

def get_current_time_utc():
    return datetime.now(timezone.utc)

class FunctionModel(Model):
    """
    A serverless function to orchestrate 
    """
    class Meta:
        table_name = FUNCTION_TABLE_NAME 
        host = HOST 
    name = UnicodeAttribute(hash_key=True) 
    resourceId = UnicodeAttribute()
    attributes = JSONAttribute()
    schedule = BinaryAttribute(null=True)
    app = UnicodeAttribute(null=True)
    status = UnicodeAttribute(null=True)
    registeredAt = UTCDateTimeAttribute(default_for_new=get_current_time_utc)
    lastUpdatedAt = UTCDateTimeAttribute(default_for_new=get_current_time_utc)

class TriggerModel(Model):
    """
    A trigger relating elements of the platform with each other
    """
    class Meta:
        table_name = TRIGGER_TABLE_NAME
        host = HOST 
    name = UnicodeAttribute(hash_key=True)
    linked_element = UnicodeAttribute(range_key=True)
    
class ScheduleModel(Model):
    """
    A schedule used for execution management for functions
    """
    class Meta:
        table_name = SCHEDULE_TABLE_NAME
        host = HOST 
    name = UnicodeAttribute(hash_key=True)
    cron = BinaryAttribute()
    associated = ListAttribute(default=[])

class Models(Enum):
    """Defines the list of models for import in other modules"""
    FUNCTION = FunctionModel
    SCHEDULE = ScheduleModel
    TRIGGER = TriggerModel 