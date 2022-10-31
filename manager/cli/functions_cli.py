"""
Implements the CLI interface to the `function` subapplication.

Functions on the chosen backend can be CRUDed and associated 
with orchestration elements, such as triggers and schedules
also managed in the system.
"""
import typer
from manager.manager import Manager
from typing import List

manager = Manager()

function_app = typer.Typer()

# Define the app interface
@function_app.command("register")
def function_create(
    arn: str = typer.Argument(
        ...,
        help="Function ARN of the function to register",
    ),

    ):
    """
    Displays the available functions not yet registered and provides the 
    user with an option to select functions to be registered in the system.
    All registered functions are then automatically monitored, and can be further
    orchestrated.
    """
    # TODO: Displey the functions not yet registered in a numbered list
    # TODO: Display a prompt allowing the user to enter the number of the function to register
    # TODO: Get the function details for the selected function
    # TODO: Write the new function entry into the backend table
    # TODO: Display an updated list of available/unregistered functions for further selection
    typer.secho(f"Putting function {arn} under orchestration")
    
@function_app.command("list")
def list_functions(
    stack_name: str = typer.Option(
        'test',
        "--stack",
        "-s",
        prompt="stack containing lambdas?",
        help="List available lambdas in a certain stack"
    ),
    attributes: List[str] = typer.Option(
        ['FunctionName', 'FunctionArn', 'Runtime'],
        "--attr",
        "-a",
        help="Set of keys to display in the function return dict"
        )
) -> None:
    """Retrieve the list of all lambdas for the given stack"""
    import json
    new_line='\n'
    functions = manager.list_functions()
    available_resources= list(set([key for f in functions for key in f.keys()]))
    typer.echo(attributes)
    filtered_return = [{k: f[k] for k in f.keys() & set(attributes)} for f in functions]
    if not all([bool(d) for d in filtered_return]):
        typer.secho(f"The filter set did not return any repsonses: Please use the following arguments only: {new_line.join(available_resources)}", fg='red')
        typer.Exit(0)
        return
    for idx, function in enumerate(filtered_return):
        typer.secho(f"{idx}) {function['FunctionName']}: {json.dumps(function, indent=2)}", fg='green')
