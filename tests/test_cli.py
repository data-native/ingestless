from typer.testing import CliRunner
from manager.cli.cli import app

runner = CliRunner()

def test_list_functions():
    result = runner.invoke(app, ["functions", "list"])

def test_function_create():
    result = runner.invoke(app, ["functions", "register"], input="5")
    assert result.exit_code == 0
    assert 'FunctionName' in result.stdout

def test_function_list_registered():
    result = runner.invoke(app, ["functions", "list-registered"])
    assert result.exit_code == 0

def test_function_schedule():
    result = runner.invoke(app, ['functions', 'schedule'])