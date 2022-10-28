"""
Implements the CLI interface to the `function` subapplication.

Functions on the chosen backend can be CRUDed and associated 
with orchestration elements, such as triggers and schedules
also managed in the system.
"""
import typer
from manager.manager import Manager

manager = Manager()

function_app = typer.Typer()

# Define the app interface
@function_app.command("register")
def function_create(trigger: str):
    typer.secho(f"Creating function {trigger}")
    
@function_app.command("list")
def list_functions(
    stack_name: str = typer.Option(
        'test',
        "--stack",
        "-s",
        prompt="stack containing lambdas?",
        help="List available lambdas in a certain stack"

    )
) -> None:
    """Retrieve the list of all lambdas for the given stack"""
    functions = manager.list_functions()
    typer.secho(functions, fg='green')