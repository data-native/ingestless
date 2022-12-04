"""
Tests the interface implementation required for the serverless
providers implemented by the executor plug-ins.

"""

import pytest
from pathlib import Path

# Import the providers
from restmap.manager.Manager import Manager
from restmap.executor.AbstractTopicProvider import AbstractTopicProvider
from restmap.executor.AWS.BaseConstructProvider import BaseConstructProvider, ConstructContextManager

# from restmap.executor.AWS.provider.bucket import BucketProvider
from restmap.executor.AWS.provider.topic import Topic, TopicProvider

@pytest.fixture
def manager():
    return Manager('AWS', 'teststack')

@pytest.fixture
def template_path():
    return Path('./ingestless/tests/restmap/assets/complex_endpoint.yml')

class TestBucketProvider:
    """
    Tests the standard interface to the bucket provider
    """
    pass

class TestFunctionProvider:
    """
    Tests the standard interface to the function provider
    """

    def test_register(self, manager: Manager):
        raise NotImplementedError

    def test_compile(self, manager: Manager):
        raise NotImplementedError

    def test_use_function(self, manager: Manager):
        raise NotImplementedError

    def test_withRole(self, manager: Manager):
        raise NotImplementedError
    
    def test_use(self,template_path: Path, manager: Manager):
        """
        Can set a context for a selected function construct to become
        the target of all following interactions with the FunctionProvider.
        """
        manager.plan(template_path)
        # function is a context manger
        target_function = manager.executor._constructs.keys()[0]
        assert isinstance(manager._executor.Function.useFunction(), ConstructContextManager)
        with manager._executor.Function.use(target_function) as f:
            # context sets the selected function onto provider._selected_construct
            assert f._selected_function, "A function was selected and set on the Provider instance"
            assert f._selected_function.uid == target_function
        # Stepping out of the context clears provider._selected_construct
        assert not manager._executor.Function._selected_function, "Exiting the context must clear the selected function in the provider"
        # All methods that where called on the function manager within the scope of the context manager are applied only to the selected construct

    def test_notify(self, template_path: Path, manager: Manager):
        """
        Can create a trigger relationship between two registered functions
        that gets natively deployed onto the backend for high-performance orchestration
        """
        # Need to parse function objects from a given template
        manager.plan(str(template_path.absolute()))
        # Need to register the functions with the provider
        dplys = manager._deployables
        manager._executor.Function.register(dplys)
        with manager._executor.Function.use(function_name) as f:
            f.notify()

    def test_trigger(self, template_path: Path, manager: Manager):
        """
        Can trigger on a given event source 
        """
        manager.plan(str(template_path.absolute()))
        # Need to register the functions with the provider
        dplys = manager._deployables
        manager._executor.Function.register(dplys)
        # Select a source to react to 
        function_name = ''
        manager._executor.Topic.register('success_topic')
        with manager._executor.Function.use(function_name) as f:
            f.trigger(on='topic', name='success_topic') 
        


class TestTopicProvider:
    """
    Tests the standard interface for managing NotificationTopics
    """

    def test_topic(self, manager: Manager):
        topic = manager._executor.Topic.topic('testtopic', {})
        assert isinstance(topic, Topic), "Topic must be returned as an abstraction enabling access to a common management interface independent of the backend implementation of the construct"
        # assert manager._executor.Topic._constructs[0] == topic.topic

    def test_use_topic(self, manager: Manager):
        topic = manager._executor.Topic.topic('testtopic', {})
        with manager._executor.Topic.use('testtopic') as t:
            assert isinstance(t, TopicProvider) 
            assert t._construct_in_scope == topic.topic
        assert not manager._executor.Topic._construct_in_scope, "After exiting the context, the manager must not have a selected_construct set"

    def test_grant_publish(self, template_path: Path, manager: Manager):
        manager.plan(template_path)
        function = manager._executor.Function._constructs
        topic = manager._executor.Topic.topic('testtopic', {})
        with manager._executor.Topic.use('testtopic') as t:
            t.grant_publish()
