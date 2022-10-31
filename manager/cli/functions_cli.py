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
from typing import List, Dict


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
    display_registered_functions()
    
@function_app.command("schedule")
def associate_schedule_to_function(
    attributes: List[str] = typer.Option(
        [],
        "--attr",
        "-a",
        help="Set of keys to display in the function return dict"
    )
):
    """
    Lists all registered functions with their current schedule set, and allows
    a selection of all functions that should have a given schedule set.
    """
    new_line = '\n'
    # List all functions
    typer.secho(f"{new_line}Schedule applications{new_line}___________________", fg='blue')
    functions = display_functions(attributes=attributes)

    # Prompt selection of all functions to have the same schedule
    selection_options = {
        'intro': 'Select applications to schedule',
        'prompt': 'Select functions as list',
        'choices': {f['FunctionName']:{}  for f in functions }
    }
    display_selection(selection_options)

    # Prompt selection of 1) CRON direct to create new schedule 2) Select existing
    schedule_options = {
        'intro': "Select your schedule",
        'prompt': "",
        'choices': {
            'existing schedules': {},
            'ad-hoc CRON': {}
        }
    }
    display_selection(schedule_options)
    # Associate schedule with all functions that have been selected

    # Return status 

#  HELPERS_____________
def display_selection(options: Dict):
    """
    Displays a set of options and records the selection.
    Retries can be specified.

    @options: A dictionary of parametrized options to handle
        @introduction: The introduction to explain the selection to take
        @prompt: The message to motivate the selection
        @choices: A dict of named options and their attributes 
        - Key: Display name of the option
        - Value: A dict of attributes to specify handling of the option
    """
    new_line = '\n'
    typer.secho(f"{new_line}{options['intro']}{new_line}", fg="blue")
    for idx, (option, attrs) in enumerate(options['choices'].items()):
        typer.secho(f'{idx}:: {option}')
    return typer.prompt(f"{new_line}>> {options['prompt']}:   ")

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

def display_registered_functions(app: str='', attributes: List[str]=[]):
    """
    Displays the functions registered with the system in a overview table.
    @app: Subsets the list to all functions registered with an application
    """
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
    title = f"{new_line}Registered functions{new_line}-------------------{new_line}Currently registered: {len(results)} Functions {scope}"
    header= " # | App | Name | FunctionHandler | Runtime "
    typer.secho(title, fg='blue')
    typer.secho(header, fg='blue')
    # Display each result in newline with index for selection
    typer.secho('-'* len(header), fg='blue')
    for idx, function in enumerate(results):
        typer.secho(f"{idx}) {function.app} |  {function.name} | {function.attributes['Handler']} | {function.attributes['Runtime']}", )