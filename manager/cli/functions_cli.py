"""
Implements the CLI interface to the `function` subapplication.

Functions on the chosen backend can be CRUDed and associated 
with orchestration elements, such as triggers and schedules
also managed in the system.
"""
import json
import typer
from manager.enums import StatusCode
from manager.manager import Manager
from manager.models import FunctionModel, ScheduleModel, TriggerModel
from typing import List


manager = Manager()

function_app = typer.Typer()

# Define the app interface
@function_app.command("register")
def function_create(
    attributes: List[str] = typer.Option(
        ['Description', 'FunctionName', 'FunctionArn', 'Runtime'],
        "--attr",
        "-a",
        help="Set of keys to display in the function return dict"
        )
    # arn: str = typer.Argument(
        # ...,
        # help="Function ARN of the function to register",
    # ),

    ):
    """
    Displays the available functions not yet registered and provides the 
    user with an option to select functions to be registered in the system.
    All registered functions are then automatically monitored, and can be further
    orchestrated.
    """
    # TODO: Displey the functions not yet registered in a numbered list
    functions = display_functions(attributes=attributes)
    # TODO: Display a prompt allowing the user to enter the number of the function to register
    selected_ids = typer.prompt("Select one or more functions to register.", type=int)
    selection = functions[selected_ids]
    # selection = [functions[id] for id in selected_ids]
    # TODO: Get the function details for the selected function
    typer.secho(selection)
    # TODO: Write the new function entry into the backend table
    status = manager.register_function(manager.models.FUNCTION(
        name=selection['FunctionName'],
        attributes = selection,
        schedule = None
    ))
    if status != StatusCode.SUCCESS:
        typer.secho("Error writing element", fg='Red')
    # TODO: Display an updated list of available/unregistered functions for further selection

    # typer.secho(f"Putting function {arn} under orchestration")
    
@function_app.command("list")
def list_all_functions(
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
    display_functions(attributes=attributes)

@function_app.command("list-registered")
def list_all_registered(
    app: str = typer.Option(
        '',
        "--app",
        "-p",
        help="Select subset of functions registered to the given application"
    ),
    attributes: List[str] = typer.Option(
        [],
        "--attr",
        "-a",
        help="Set of keys to display in the function return dict"
    )):
    """Retrieve the list of registered functions in the orchestrator"""
    new_line = '\n'
    results = manager.list_registered_functions()
    
    # if attributes:
        # results = [{k: f[k] for k in f.keys() & set(attributes)} for f in results]
        # if not all([bool(d) for d in results]):
            # typer.secho(f"The filter set did not return any repsonses: Please use the following arguments only:{new_line} {new_line.join(available_resources)}", fg='red')
            # typer.Exit(0)
            # return
    # TODO: Display results as table
    scope = "in total" if app == '' else f"for {app}"
    typer.secho(f"{new_line}Registered functions{new_line}-------------------{new_line}Currently registered: {len(results)} Functions {scope}", fg='green')
    # Display each result in newline with index for selection
    typer.secho("App | Name | FunctionHandler | Runtime ")
    for idx, function in enumerate(results):
        typer.secho(f"{idx}) {function.name} | {function.attributes['Handler']} | {function.attributes['Runtime']}", )
    

def display_functions(attributes:List[str]=[]) -> List[dict]:
    """Displays a the list of available functions to the cli"""
    new_line='\n'
    results = []
    functions = manager.list_functions()
    # Conditionally filter based on set keys
    available_resources= list(set([key for f in functions for key in f.keys()]))
    if attributes:
        results = [{k: f[k] for k in f.keys() & set(attributes)} for f in functions]
        if not all([bool(d) for d in results]):
            typer.secho(f"The filter set did not return any repsonses: Please use the following arguments only:{new_line} {new_line.join(available_resources)}", fg='red')
            typer.Exit(0)
            return []
    for idx, function in enumerate(results):
        typer.secho(f"{idx}) {function['FunctionName']}: {json.dumps(function, indent=2)}", fg='green')
    return functions