from configparser import ConfigParser
from pathlib import Path
import logging
import threading
import typer
from typing import List

from manager import __app_name__
from manager.enums import StatusCode
from manager.models import FunctionModel, ScheduleModel, TriggerModel

# Set Configuraton parameters
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

# Table configuration
REGISTERED_TABLES = [FunctionModel, ScheduleModel, TriggerModel]

def init_parser(path: str) -> ConfigParser:
    """Load configuration"""
    parser = ConfigParser()
    parser.read(path or CONFIG_FILE_PATH)
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

def _reset_database() -> StatusCode:
    """
    Drops all tables and recreates a clean state for
     the application.
    """
    for table in REGISTERED_TABLES:
        try:
            table.delete_table()
        except Exception as e:
            return StatusCode.DB_WRITE_ERROR
    _init_database()
    return StatusCode.SUCCESS

def _reset_application() -> StatusCode:
    """
    Clears the application state
    """
    #TODO: Implement clean up of application state
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
    threads = []
    for table in REGISTERED_TABLES:
        if not table.exists():
            thread = threading.Thread(target=table.create_table, kwargs={'read_capacity_units':1, 'write_capacity_units': 1})
            threads.append(thread)

    # Execute table creation
    for thread in threads:
        thread.start()
        
    return StatusCode.SUCCESS

# Initializing the parser
parser = init_parser('../config.ini')
