import typer

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
    typer.secho('List of lambda', fg='green'
    )