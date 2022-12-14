"""
Implements the CLI interface to the `function` subapplication.

Functions on the chosen backend can be CRUDed and associated 
with orchestration elements, such as triggers and schedules
also managed in the system.
"""
import logging
import typer
import pickle
from cron_converter import Cron
from typing import List, Dict
from tabulate import tabulate

from enums import StatusCode
from manager.manager import Manager
from manager.models import FunctionModel, ScheduleModel, TriggerModel
from manager.cli import utils

logger = logging.getLogger('root')

manager = Manager()

function_app = typer.Typer()

# HELPER FUNCTIONS_____________
#TODO: Extract to utils

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
    ids = typer.prompt("Select one or more functions to register.", type=str)
        
    ids = utils.get_argument_list(ids, type=int)

    # TODO: Write the new function entry into the backend table
    if typer.confirm(f"Register functions {ids}"):
        for id in ids:
            selection = functions[id]
            typer.secho(selection)
            status = manager.register_function(manager.models.FUNCTION(
                name=selection['FunctionName'],
                resourceId=selection['FunctionArn'],
                attributes = selection,
                schedule = None,
                status = None,
            ))
            if status != StatusCode.SUCCESS:
                typer.secho("Error writing element", fg='Red')

    # typer.secho(f"Putting function {arn} under orchestration")
    
@function_app.command("list-available")
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

@function_app.command("list")
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

@function_app.command("remove") 
def unregister_function(
    name: str = typer.Option(
        '',
        "--name",
        "-n",
        help="Name of the function to remove"
    )):
    """Remove a function from the registry"""
    functions = display_registered_functions()
    select_idx = typer.prompt("Which function(s) to remove:", type=str)
    select_idx = utils.get_argument_list(select_idx, type=int)
    for idx in select_idx:
        function = functions[idx]
        manager.unregister_function(function.name)

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
    functions = manager.list_registered_functions()

    # Prompt selection of all functions to have the same schedule
    selection_options = {
        'intro': 'Select applications to schedule',
        'prompt': 'Select functions as list',
        'choices': {f.name: {
            'attributes': [f.name, f.status, f.schedule, f.schedule],
        }  for f in functions},
        'headers': ['idx', 'Function Name', 'Status', 'Schedule', 'CRON'],
        'type': str
    }
    selected_function_idx = display_selection(selection_options)
    selected_function_idx = utils.get_argument_list(selected_function_idx, type=int)

    typer.confirm(f"So you want to schedule functions: {selected_function_idx}")
    # Get the selected funtions
    # Prompt selection of 1) CRON direct to create new schedule 2) Select existing
    schedule_options = {
        'intro': "Select your schedule",
        'prompt': "",
        'choices': {
            'existing schedules': {},
            'ad-hoc CRON': {},
            'unschedule': {},
            'flipStatus': {},
        },
        'headers': ['idx', 'Option'],
        'type': int
    }

    selected = None 
    method = None
    schedule = None
    while not selected: 
        method = display_selection(schedule_options)
        if method == 0:
            # Ensure schedules are available to select from
            schedules = manager.list_schedules()
            if not schedules:
                typer.secho('No registered schedules to choose from. Please define a new one')
            # display existing schedules
            display_schedules(schedules=schedules)
            # Make a selection which one to apply
            schedule_idx = typer.prompt("Select a schedule to apply: ", type=int)
            schedule = schedules[schedule_idx]
            selected = True
        elif method == 1 : 
            # Create a Schedule object with new cron
            registration_status = None
            while registration_status != StatusCode.SUCCESS:
                if registration_status:
                    # Has previously failed and status was set
                    typer.secho("Registration failed: Please check your parameter carefully and try again", fg='red')
                typer.secho("Create new schedule", fg='green')
                name = typer.prompt(">> Name: ")
                cron = Cron(typer.prompt(">> CRON schedule [mhdwy]: ", type=str))
                schedule = ScheduleModel(name, cron=cron, associated=[])
                registration_status = manager.register_schedule(schedule)
            selected = True
        elif method == 2 or method == 3:
            # TODO: Find a way to include method 2/3 into scheduling operation
            selected = True

    for idx in selected_function_idx:
        selected_function = functions[idx]
        logger.info("Selected functions", selected_function)
        if method == 0 or method == 1:
            manager.schedule_function(schedule.name, function_hk=selected_function.name)
        elif method == 2:
            # Unschedule a function
            manager.unschedule_function(selected_function.name)
        elif method == 3:
            # Flip schedules
            manager.toggle_event_status(selected_function.name)
        typer.Exit(0)

@function_app.command("describe") 
def describe_function(
    name: str = typer.Option(
        '',
        "--name",
        "-n",
        help="Name of the function to describe"
    )):
    """
    Describes the details for a chosen function
    """
    import json
    function = manager.describe_function(name)
    typer.echo(json.dumps(function, indent=4))
    

#  HELPERS_____________
def display_schedules(schedules: List[ScheduleModel]) -> StatusCode:
    """
    Displays the list of registered schedules to the screen.

    @options: A 
    """
    new_line = '\n'
    result_table = []
    headers= ["idx", "Name", "Schedule", "Associated functions"]
    if not schedules:
        typer.secho("No schedules registered. Please register a new schedule now.")
        return StatusCode.DB_READ_ERROR
    for schedule in schedules:
        name = schedule.name
        cron = pickle.loads(schedule.cron)
        associated = schedule.associated
        result_table.append([ name, cron.to_string(), associated])
    # Display table
    typer.secho(f"{new_line}Registered Schedules", fg='blue')
    typer.echo(tabulate(result_table, headers=headers, showindex='always')) 
    return StatusCode.SUCCESS

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
    if any(['attributes' in option for option in options['choices'].values()]):
        typer.echo(tabulate([v['attributes']  for k,v in options['choices'].items()],headers=options['headers'], showindex='always'))
    else:
        typer.echo(tabulate([[choice] for choice in options['choices']],headers=options['headers'], showindex='always'))

    # for idx, (option, attrs) in options['choices'].items():
        # typer.secho(f'{idx}:: {option}')
    selection = typer.prompt(f"{new_line}>> {options['prompt']}:  ", type=options.get('type', str))
    print("Selection taken: ", selection)
    return selection

def display_functions(attributes:List[str]=[]) -> List[dict]:
    """Displays a the list of available functions to the cli"""
    new_line='\n'
    results = []
    result_table = []
    functions = manager.list_functions()
    if functions:
        # Conditionally filter based on set keys
        available_resources= list(set([key for f in functions for key in f.keys()]))
        if attributes:
            results = [{k: f[k] for k in f.keys() & set(attributes)} for f in functions]
            if not all([bool(d) for d in results]):
                typer.secho(f"The filter set did not return any repsonses: Please use the following arguments only:{new_line} {new_line.join(available_resources)}", fg='red')
                typer.Exit(0)
                return []
        for function in results:
            result_table.append(function)
            # typer.secho(f"{idx}) {function['FunctionName']}: {json.dumps(function, indent=2)}", fg='green')
        typer.secho(f"{new_line}Total Available Functions: {len(functions)}", fg='blue')
        if attributes:
            typer.secho(f"Applied {len(attributes)} column filters: {', '.join(attributes)}", fg='green')
            typer.secho(f"Available attributes: {set(available_resources).difference(set(attributes))} {new_line}")
        typer.echo(tabulate(result_table, headers='keys', showindex='always'))
        return functions
    return []

def display_registered_functions(app: str='', attributes: List[str]=[]):
    """
    Displays the functions registered with the system in a overview table.
    @app: Subsets the list to all functions registered with an application
    """
    new_line = '\n'
    registered_functions = manager.list_registered_functions()
    
    # if attributes:
        # results = [{k: f[k] for k in f.keys() & set(attributes)} for f in results]
        # if not all([bool(d) for d in results]):
            # typer.secho(f"The filter set did not return any repsonses: Please use the following arguments only:{new_line} {new_line.join(available_resources)}", fg='red')
            # typer.Exit(0)
            # return
    # TODO: Display results as table
    headers = ["#", "App","Name","FunctionHandler", "Runtime", "Schedule","[mhdWmY]", "Status", "ResourceId"]
    result_table = []
    
    scope = "" if app == '' else f"for {app}"
    title = f"{new_line}Registered functions{new_line}-------------------{new_line}Currently registered: {len(registered_functions)} Functions {scope}"
    typer.secho(title, fg='blue')
    # Conditionally manage non existance of schedules on functions 
    cron = '/'
    schedule_name = '/'
    for function in registered_functions:
        # TODO: Get the details for the associated schedule
        if function.schedule:
            #TODO: Extract status from schedule
            schedule_meta = manager.describe_schedule(function.schedule.name)
            cron = function.schedule.cron.to_string()
            schedule_name = function.schedule.name
        result_table.append([
            function.app, 
            function.name, 
            function.attributes.get('Handler', 'Not set'), 
            function.attributes.get('Runtime', 'Not Set'), 
            schedule_name, 
            cron, 
            function.status,
            function.resourceId
        ])
    typer.echo(tabulate(result_table, headers=headers, showindex='always'))
    return registered_functions
