"""
Tests the utility functions for the AWSProvider
"""
import pytest
from cron_converter import Cron
from manager.provider.AWS import utils

def test_compile_schedule_expression():
    """
    Ensures returned string is compatible with ScheduleExpression parameter
    for the EventBus API.
    """
    # Prepare a cron object
    thirty_sec_trigger = Cron('1/2 * * * *')
    minute_trigger = Cron('1 * * * *')
    five_minute_trigger = Cron('5 * * * *')

    # Schedules raise if limits are hit
    assert "cron(1 * * * ? *)" == utils.compile_schedule_expression(thirty_sec_trigger)
    

    # Schedules comply with formatting rules
    assert "cron(1 * * * ? *)" == utils.compile_schedule_expression(minute_trigger)
    assert "cron(5 * * * ? *)" == utils.compile_schedule_expression(five_minute_trigger)


