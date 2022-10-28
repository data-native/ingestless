from typer import secho
from textwrap import dedent

def secho(text: str, highlight:str) -> None:
    return typer.secho(dedent(text))