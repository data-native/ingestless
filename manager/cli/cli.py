from typing import Optional
import typer

from manager import __app_name__, __version__
from manager import config
from manager.enums import StatusCode, Errors

from manager.cli.trigger_cli import trigger_app
from manager.cli.functions_cli import function_app
from manager.cli.schedules_cli import schedule_app

# Define the app interface
app = typer.Typer()
app.add_typer(function_app, name="functions")
app.add_typer(schedule_app, name="schedules")
app.add_typer(trigger_app, name="triggers")

# Define general methods
def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.command()
def version  (
    version: Optional[bool] = typer.Option(
        None, 
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True
    )
) -> None:
    return

@app.command()
def init(
    
) -> None:
    """Initialize the application"""
    app_init_status = config.init_app() 
    if app_init_status != StatusCode.SUCCESS:
        typer.secho(
            f'Creating config file failed with "{Errors[app_init_status]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            'Successfully completed setup of the application.', fg='green'
        )

