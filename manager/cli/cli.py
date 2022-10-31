from typing import Optional
import typer
import textwrap

from manager import __app_name__, __version__
from manager import config
from manager.enums import StatusCode, Errors, Provider

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
    
) -> StatusCode:
    """Initialize the application"""
    new_line = '\n'
    # Initial Screen ======
    typer.secho(textwrap.dedent(
    """
    --------- I N G E S T L E S S ----------- 
    The serverless data ingestion orchestration framework,
    that hyperscales your ingest and downscales your cost.

    We are getting ready to set up the orchestration manager
    """), fg='green')

    selected_provider = Provider(int(typer.prompt(
    textwrap.dedent(f""" Please select the backend platform:
    {''.join([f"{new_line}{idx+1}) {provider.name}" for idx, provider in enumerate(Provider)])}
    """))))
    typer.secho(f"Initializing state manager for {selected_provider.name}")

    # Configuring application 
    app_config_status = config.config_app(provider=selected_provider)
    # Initializing application based on configuration presets
    app_init_status = config.init_app(provider=selected_provider) 
    return app_init_status

@app.command('reset')
def reset(

) -> None:
    """
    Resets the application to a clean state.
    
    Drops all used tables, discarding all historical application 
    state and system logs. 
    """
    confirmation = typer.confirm("Do you want to completely delete the application state?")
    if confirmation:
        typer.secho("Deleting application state", fg='green')
        config._reset_application()
        typer.secho("Dropping application tables", fg='green')
        reset_status = config._reset_database()
        
    typer.Exit(0)