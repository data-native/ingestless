"""
Tests the interface implementation required for the serverless
providers implemented by the executor plug-ins.

"""

import pytest
from pathlib import Path

# Import the providers
from restmap.manager.Manager import Manager
from restmap.executor.AWS.provider.function import FunctionContextManager
# from restmap.executor.AWS.provider.bucket import BucketProvider

pytest.fixture
def manager():
    return Manager('AWS', 'teststack')

@pytest.fixture
def template_path():
    return Path('./tests/restmap/assets/templates/complex_endpoint.yml')
    

class TestBucketProvider:
    """
    Tests the standard interface to the bucket provider
    """
    pass

class TestFunctionProvider:
    """
    Tests the standard interface to the function provider
    """

    def test_register(manager: Manager):
        raise NotImplementedError

    def test_compile(manager: Manager):
        raise NotImplementedError

    def test_use_function(manager: Manager):
        raise NotImplementedError

    def test_withRole(manager: Manager):
        raise NotImplementedError
    
    def test_using_function(manager: Manager):
        """
        Can set a context for a selected function construct to become
        the target of all following interactions with the FunctionProvider.
        """
        manager.plan()
        # function is a context manger
        target_function = manager.executor._constructs.keys()[0]
        assert isinstance(manager._executor.Function.useFunction(), FunctionContextManager)
        with manager._executor.Function.useFunction(target_function) as f:
            # context sets the selected function onto provider._selected_construct
            assert f._selected_function, "A function was selected and set on the Provider instance"
            assert f._selected_function.uid == target_function
        # Stepping out of the context clears provider._selected_construct
        assert not manager._executor.Function._selected_function, "Exiting the context must clear the selected function in the provider"
        # All methods that where called on the function manager within the scope of the context manager are applied only to the selected construct



    def test_triggers(template_path: Path, manager: Manager):
        """
        Can create a trigger relationship between two registered functions
        that gets natively deployed onto the backend for high-performance orchestration
        """
        # Need to parse function objects from a given template
        manager.plan(str(template_path.absolute()))
        # Need to register the functions with the provider
        dplys = manager._deployables
        manager._executor.Function.register(dplys)
        
        manager._executor.Function.triggers

