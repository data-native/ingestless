"""
Utility methods to work with the function Models 
in pynamodb
"""
import pickle
from manager.models import FunctionModel, ScheduleModel

def load_function_instance(function: FunctionModel) -> FunctionModel:
    """
    Fully loads a FunctionModel into unpickled state when reading
    from database
    """
    if function.schedule:
        if isinstance(function.schedule, bytes):
            function.schedule = pickle.loads(function.schedule)
        if isinstance(function.schedule.cron, bytes):
            function.schedule.cron = pickle.loads(function.schedule.cron)
    return function

def load_schedule_instance(schedule: ScheduleModel) -> ScheduleModel:
    """
    Fully loads a FunctionModel into unpickled state when reading
    from database
    """
    if schedule.cron:
        if isinstance(schedule.cron, bytes):
            schedule.cron = pickle.loads(schedule.cron)
    return schedule
