import typer
import pickle
import logging
from typing import List
from cron_converter import Cron
from tabulate import tabulate

from manager.manager import Manager
from manager.models import ScheduleModel
from manager.types import ScheduleItem
from manager.cli import utils

logger = logging.getLogger('root')

schedule_app = typer.Typer()

# Constants
CRON_SCHEMA = "[mhDWMY]"

manager = Manager()

# Define the app interface
@schedule_app.command("create")
def schedule_create():
    """
    Iteratively create a schedule, confirm the cron timing table and commit it to the backend.
    Designed to iterate over passed CRON strings until they are correctly formated and confirmed by user.
    """
    name = typer.prompt("Schedule name")
    confirmed=False
    while not confirmed:
        valid_cron = False 
        while not valid_cron: 
            schedule = typer.prompt(f"Schedule as CRON {CRON_SCHEMA}")
            try:
                cron = Cron(schedule, {
                    'output_weekday_names': True,
                    'output_month_names': True
                })
                valid_cron = True
                # Create output for confirmation
                schedule_print = zip(['minute', 'hour', 'day', 'month', 'day of week', 'year'][:len(cron.to_list())], cron.to_list())
                confirmed = typer.confirm(f"You want to schedule for:\n{tabulate(schedule_print)}")
                if confirmed:
                    try:
                        schedule = manager.models.SCHEDULE(name, cron=pickle.dumps(cron))
                        manager.register_schedule(schedule)
                    except Exception as e:
                        typer.secho(f'Unable to register schedule: {e}', fg='red')
                        typer.Exit(1)
                    typer.secho(f'Successfully created schedule {name}: {cron}', fg='green')
                    typer.Exit(0)
            except ValueError:
                typer.secho(f"The cron: {schedule} is in an incorrect format. Please provide again.")

            typer.secho(f"Creating schedule {schedule}", fg="green")

@schedule_app.command("list")
def schedule_list_all() -> List[ScheduleModel]:
    """
    Displays all registered schedules for management
    """
    new_line = '\n'
    schedules = manager.list_schedules()
    typer.secho(f"{new_line}Registered a total of : {len(schedules)} schedules")
    typer.echo("----------------------------------------------------")
    typer.secho(f"Schedule Name | CRON | # of associated functions")
    for schedule in schedules:
        cron = pickle.loads(schedule.cron)
        typer.secho(f"{schedule.name} | { cron } | {schedule.associated}")
    return schedules

@schedule_app.command("remove") 
def remove_schedule(
):
    """
    Deletes a registered schedule from the system
    """
    schedules = schedule_list_all()

    ids = typer.prompt("Which schedules to delete?", type=str)
    ids = utils.get_argument_list(ids, type=int)
    if typer.confirm(f"You sure you want to remove schedules: {ids}? y/N"):
        for id in ids:    
            selected_schedule = schedules[id]
            manager.unregister_schedule(selected_schedule.name)
            logger.debug(f'Removed schedule {selected_schedule.name}')
