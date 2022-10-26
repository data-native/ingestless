import configparser
from pathlib import Path

import typer

from manager import __app_name__
from manager.enums import StatusCode


CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

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
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": name }
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return StatusCode.DB_WRITE_ERROR
    return StatusCode.SUCCESS
