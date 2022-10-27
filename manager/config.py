from configparser import ConfigParser
from pathlib import Path

import typer

from manager import __app_name__
from manager.enums import StatusCode
from manager.models import FunctionModel, ScheduleModel, TriggerModel

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
    # Load data
    parser = ConfigParser()
    with open('../config.ini') as f:
        parser.read_file(f)
    
    # Ensure tables are initialized
    if not TriggerModel.exists():
        TriggerModel.create_table(billing_mode="PAY_PER_REQUEST", wait=True)
    if not FunctionModel.exists():
        FunctionModel.create_table(billing_mode="PAY_PER_REQUEEST", wait=True)
    if not ScheduleModel.exists(): 
        ScheduleModel.create_table(billing_mode="PAY_PER_REQUEEST", wait=True)
    
    return StatusCode.SUCCESS

# Initializing the parser
parser = init_parser('../config.ini')
