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
from manager.provider.AWSProvider import AWSProvider
from manager.provider.abstract_provider import BackendProvider

#TODO: Integrate into the management class
# Configure logging
logging.basicConfig(level=logging.INFO)

# Set Configuraton parameters
CONFIG_DIR_PATH = Path('./manager') 
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

# Table configuration
REGISTERED_TABLES = [FunctionModel, ScheduleModel, TriggerModel]

class ConfigManager:
    def __init__(self) -> None:
        self.configuration = self._read_config()

    def _read_config(self):
        "Reads configuration"
        config = ConfigParser()
        config.read(CONFIG_FILE_PATH)
        logging.info(f"Read Configuration as: {config}")
        return config
    
    def provider(self):
        "Get the configured backend provider"
        provider_config =  self.configuration['DEFAULT']['provider']
        logging.info(f"Set selected provider: {provider_config}")
        return Provider[provider_config]
        
def init_parser(path: str) -> ConfigParser:
    """Load configuration"""
    parser = ConfigParser()
    parser.read(path or CONFIG_FILE_PATH)
    return parser

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
        logging.info(f"Selected to configure orchestration for a Stack: {stack}")

    logging.info("Successfully completed application configuration")
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
    aws_provider = AWSProvider() 
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
    logging.info("Resetting the database")
    errors = None
    for table in REGISTERED_TABLES:
        try:
            table.delete_table()
            logging.info(f"Deleted table: {table}")
        except Exception as e:
            error = StatusCode.DB_WRITE_ERROR
    _init_database()
    
    return errors or StatusCode.SUCCESS

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
    logging.info("Initializing Database Tables")
    # Ensure tables are initialized
    threads = []
    for table in REGISTERED_TABLES:
        if not table.exists():
            # table.create_table(write_capacity_units=1, read_capacity_units=1)
            thread = threading.Thread(target=table.create_table, kwargs={'read_capacity_units':1, 'write_capacity_units': 1})
            threads.append(thread)

    # Execute table creation
    for thread in threads:
        thread.start()
        
    return StatusCode.SUCCESS

