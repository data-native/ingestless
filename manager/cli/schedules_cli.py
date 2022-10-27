import typer
from cron_converter import Cron
from tabulate import tabulate

from manager.manager import Manager
from manager.types import Schedule

schedule_app = typer.Typer()

# Constants
CRON_SCHEMA = "[mhDWMY]"

manager = Manager()

# Define the app interface
@schedule_app.command("create")
def schedule_create():
    name = typer.prompt("Schedule name")
    #TODO: Implement cron parser
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
            except ValueError:
                typer.secho(f"The cron: {schedule} is in an incorrect format. Please provide again.")
        # Create output for confirmation
        schedule_print = zip(['minute', 'hour', 'day', 'month', 'day of week', 'year'][:len(cron.to_list())], cron.to_list())

        confirmed = typer.confirm(f"You want to schedule for:\n{tabulate(schedule_print)}")

    typer.secho(f"Creating schedule {schedule}", fg="green")

    #TODO: Call scheduler with specified details
    schedule = Schedule(name, cron)
    try:
        manager.register_schedule(schedule)
    except Exception as e:
        typer.secho(f'Unable to register schedule: {e}', fg='red')
        typer.Exit(1)
    typer.secho(f'Successfully created schedule {name}: {cron}', fg='green')
    typer.Exit(0)