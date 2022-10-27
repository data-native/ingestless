import typer

trigger_app = typer.Typer()

# Define the app interface
@trigger_app.command("create")
def trigger_create(trigger_name: str):
    typer.secho(f"Creating trigger {trigger_name}")
