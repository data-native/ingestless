from configparser import ConfigParser
from pathlib import Path
import logging
import threading

import typer

from manager import __app_name__
from manager.enums import StatusCode
from manager.models import FunctionModel, ScheduleModel, TriggerModel

# Configure Configuraton parameters
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

def init_parser(path: str) -> ConfigParser:
    """Load configuration"""
    parser = ConfigParser()
    parser.read(path)
    return parser

def init_app() -> StatusCode:
    """Initialize the application"""
    config_code = _init_config_file()
    if config_code != StatusCode.SUCCESS:
        return config_code
    database_code = _init_database()
    if database_code != StatusCode.SUCCESS:
        return database_code
    return StatusCode.SUCCESS

def _init_config_file() -> StatusCode:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return StatusCode.DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except FileExistsError:
        return StatusCode.FILE_ERROR
    return StatusCode.SUCCESS

def _init_database(
    name: str = "TestDB"
) -> StatusCode:
    """
    Initialize the metadata storage table for the application.
    #TODO: Define the parameters to use and the table design to apply
    @xxx
    """

    # Ensure tables are initialized
    t1 = threading.Thread(target=TriggerModel.create_table, kwargs={'read_capacity_units':1, 'write_capacity_units': 1,  'wait':True})
    t2 = threading.Thread(target=FunctionModel.create_table, kwargs={'read_capacity_units':1, 'write_capacity_units': 1,  'wait':True})
    t3 = threading.Thread(target=ScheduleModel.create_table, kwargs={'read_capacity_units':1, 'write_capacity_units': 1,  'wait':True})

    if not TriggerModel.exists():
        t1.start()
    if not FunctionModel.exists():
        t2.start()
    if not ScheduleModel.exists(): 
        t3.start()

    
    return StatusCode.SUCCESS

# Initializing the parser
parser = init_parser('../config.ini')
