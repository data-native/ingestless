import typer
from cron_converter import Cron
from tabulate import tabulate

from manager.manager import Manager
from manager.types import ScheduleItem

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
                try:
                    schedule = ScheduleItem(name, cron)
                    manager.register_schedule(schedule)
                except Exception as e:
                    typer.secho(f'Unable to register schedule: {e}', fg='red')
                    typer.Exit(1)
                typer.secho(f'Successfully created schedule {name}: {cron}', fg='green')
                typer.Exit(0)
            except ValueError:
                typer.secho(f"The cron: {schedule} is in an incorrect format. Please provide again.")

            typer.secho(f"Creating schedule {schedule}", fg="green")