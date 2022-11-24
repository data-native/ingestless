import pytest
from typer.testing import CliRunner
from manager.manager import Manager
from manager.cli.cli import app

runner = CliRunner()

@pytest.fixture
def manager() -> Manager:
    return Manager()

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
    result = runner.invoke(app, ['functions', 'schedule'], input='0\n')

def test_remove_schedule():
    runner.invoke(app, ['schedules', 'create'], input='testschedule\n5 * * * *\ny\n')
    result = runner.invoke(app, ['schedules', 'remove'], input='0\n')
    assert result.exit_code == 0

def test_function_remove():
    # Setup
    runner.invoke(app, ['functions', 'register'], input='0\n')
    # Call functions
    result = runner.invoke(app, ['functions', 'remove'], input='0\n')
    assert result.exit_code == 0

# HELPERS__________
def test_display_registered_functions():
    from manager.cli.functions_cli import display_registered_functions
    response = display_registered_functions()
    assert isinstance(response, list)

def test_display_selection(manager: Manager):
    from manager.cli.functions_cli import display_selection
    functions = manager.list_registered_functions()
    selection_options = {
        'intro': 'Select applications to schedule',
        'prompt': 'Select functions as list',
        'choices': {f.name: {
            'attributes': [f.name, f.status, f.schedule.name, f.schedule.cron.to_string()],
        }  for f in functions},
        'headers': ['idx', 'Function Name', 'Status', 'Schedule', 'CRON'],
        'type': str
    }
    response = display_selection(selection_options)
    assert functions