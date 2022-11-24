"""
AWS Provider specific helper function utilities
"""
from cron_converter import Cron

# SERVICE_________EVENT BUS
def compile_schedule_expression(cron: Cron) -> str:
    """
    Compiles a cron object into the ServiceBus compatible ScheduleExpression string

    Cron objects use format [mhdmw] while ScheduleExpression uses [mhdmWy]
    [Documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)


    Restrictions:
    
    * The schedule must not be more frequent than every 1 minute
    * Format [smd]
    """
    # TODO: Findd a way to extend scheduling to years (Not supported by cron-converter)
    # TODO: Validate that the schedule is above 1 minute intervals
    
    # Ensure that * Wildcard is not used in Day-Of-Month and Day-of-Week. If so set one to ?
    m, h, d, M, w = cron.to_string().split(' ')
    # Ensure interval is above 1 minute
    if all([i == '*' for i in [m, h]]):
        m = '1'
    # Only day-of-month or day-of-week can be set to *
    if d == '*' and w == '*':
        w = '?'

    schedule_string = ' '.join([m, h, d, M, w, '*'])    

    schedule_string = f"cron({schedule_string})"
    
    return schedule_string