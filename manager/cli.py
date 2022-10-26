from typing import Optional
import typer

from manager import __app_name__, __version__
from manager import config
from manager.enums import StatusCode, Errors

app = typer.Typer()

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


@app.command()
def list(
    stack_name: str = typer.Option(
        'test',
        "--stack",
        "-s",
        prompt="stack containing lambdas?",
        help="List available lambdas in a certain stack"

    )
) -> None:
    """Retrieve the list of all lambdas for the given stack"""
    typer.secho('List of lambda', fg='green'
    )