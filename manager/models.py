from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute 

from manager.config import parser

#TODO: Automatically set dev and production env variable based on operating system
env = 'dev'

HOST = parser[env]['dynamodb_host']
FUNCTION_TABLE_NAME = parser['DEFAULT']['function_table_name']
SCHEDULE_TABLE_NAME = parser['DEFAULT']['schedule_table_name']
TRIGGER_TABLE_NAME = parser['DEFAULT']['trigger_table_name']

class FunctionModel(Model):
    """
    A serverless function to orchestrate 
    """
    class Meta:
        table_name = FUNCTION_TABLE_NAME
        host = HOST
    name = UnicodeAttribute(hash_key=True) 
    arn = UnicodeAttribute()
    schedule = UnicodeAttribute()

class TriggerModel(Model):
    """
    A trigger relating elements of the platform with each other
    """
    class Meta:
        table_name = TRIGGER_TABLE_NAME
        host = HOST
    name = UnicodeAttribute(hash_key=True)
    linked_element = UnicodeAttribute(range_key=True)
    trigger_element_arn = UnicodeAttribute()
    
class ScheduleModel(Model):
    """
    A schedule used for execution management for functions
    """
    class Meta:
        table_name = SCHEDULE_TABLE_NAME
        host = HOST
    name = UnicodeAttribute(hash_key=True)
    cron = UnicodeAttribute()
    
    