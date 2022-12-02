"""
Tests the implementation of the base functionality
against all registered backend executors. 

TODO Generalize the test to apply to a list of registered executors
TODO Set a configuration file to allow the specification of all registered providers in the system
TODO 
"""
import pytest
from pathlib import Path

from restmap.manager.Manager import Manager
from restmap.executor.AWS.AWSExecutor import AWSExecutor
from restmap.executor.AbstractBucketProvider import AbstractBucketProvider
from restmap.executor.AbstractFunctionProvider import AbstractFunctionProvider
from restmap.executor.AbstractTableProvider import AbstractTableProvider
from restmap.executor.AbstractBaseExecutor import AbstractBaseExecutor

pytest.fixture
def aws_executor():
    return AWSExecutor('teststack')

pytest.fixture
def manager():
    return Manager(executor='AWS', name='testStack')

@pytest.fixture()
def template_path():
    return Path('./ingestless/tests/restmap/assets/complex_endpoint.yml')

pytest.fixture
def init_manager(template_path: Path):
    manager = Manager(executor='AWS', name='testStack')
    manager.plan(str(template_path.absolute()))


class TestBaseFunctionality:

    def can_init(aws_executor: AWSExecutor):
        assert aws_executor
        assert isinstance(aws_executor, AbstractBaseExecutor)


class TestProviderIntegration:
    def test_has_bucket_provider(aws_executor: AWSExecutor):
        assert aws_executor.Bucket
        assert isinstance(aws_executor.Bucket, AbstractBucketProvider)

    def test_has_function_provider(aws_executor: AWSExecutor):
        assert aws_executor.Function
        assert isinstance(aws_executor.Function, AbstractFunctionProvider)

    def test_has_table_provider(aws_executor: AWSExecutor):
        assert aws_executor.Table
        assert isinstance(aws_executor.Table, AbstractTableProvider)


class CompilationManagement:
    def test_can_compile(template_path: Path, manager: Manager, aws_executor: AWSExecutor):
        resolution_graph = manager._parser.load(template_path)
        aws_executor.compile(resolution_graph)

    def test_can_deploy(template_path: Path, manager: Manager, aws_executor: AWSExecutor):
        aws_executor.plan(str(template_path.absolute()))
        aws_executor.deploy

