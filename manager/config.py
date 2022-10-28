from configparser import ConfigParser
from pathlib import Path
import logging
import threading
import typer
import textwrap
from typing import List

from manager import __app_name__
from manager.enums import StatusCode, Provider
from manager.models import FunctionModel, ScheduleModel, TriggerModel
from manager.provider import BackendProvider

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

#Uti


def config_app(
    provider: Provider
) -> StatusCode:
    """
    Configures the application based on the selected provider.
    
    This sets common standards, and allows the user to customize
    the application defaults in the configuration file in a guided
    configuration process.

    * Should a stack be orchestrated, or seperate functions selected across stacks
    * What profile should be used to authenticate 
    """
    new_line = '\n'
    typer.secho(textwrap.dedent(f"""
    {new_line} Configuring the application configuration
    """))
    #Variables to be defined
    region, stack, test = None, None, None
    # Authorization
    # Check if configuration is available for the selected 
    if typer.prompt("Shall we orchestrate a Stack? [y/n]") == 'y':
        # Get list of available stacks from the account
        stack = typer.prompt

    return StatusCode.SUCCESS

def init_app(
    provider: Provider
) -> StatusCode:
    """Initialize the application"""
    init_provider_default_config = {
        Provider.AWS: _init_aws_config,
        Provider.AZURE: _init_azure_config,
        Provider.GCP: _init_gcp_config,
        Provider.CLOUDNATIVE: _init_cloudnative_config
    }

    typer.secho("Initializing Configuration file", fg='green')
    # Ensure config file exists
    config_code = _init_config_file()
    if config_code != StatusCode.SUCCESS:
        return config_code
    # Configure config file for provider specific defaults
    init_provider_default_config[provider]()
    typer.secho("Initializing database tables", fg='green')
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

# Configuration settings across providers
def _init_aws_config() -> StatusCode:
    aws_provider = BackendProvider.new(Provider.AWS)
    aws_provider.get_configuration()
    return StatusCode.SUCCESS

def _init_azure_config() -> StatusCode:
    return StatusCode.SUCCESS

def _init_gcp_config() -> StatusCode:
    return StatusCode.SUCCESS

def _init_cloudnative_config() -> StatusCode:
    return StatusCode.SUCCESS

# Reset operations
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
 
# Initialization
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
