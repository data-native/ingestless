
"""
"""
import pytest
from restmap.manager.Manager import Manager
from restmap.orchestrator.BaseOrchestrator import IteratorNode


@pytest.fixture
def manager():
    return Manager('AWS', 'TestStack')

@pytest.fixture
def function():
    return 


class TestEventGridOrchestrator:
    """
    The event grid orchestrator implements an AWS native orchestration
    geared towards high scalability with minimal cost footprint through 
    the use of native coordination and integration services build on top
    of the EventGrid backbone.

    Main features ensured by the tests
    ----------------------------------
    * Can schedule functions with repeating time based triggers 
    * Can trigger execution lineages based on function dependencies
    * Can keep and update state of the function execution 
    * Can plan and execute parallelized execution fan-outs across a parameter space against an endpoint
    * Can keep shared endpoint state to allow coordinated activity management such as throttling against an endpoint
    """

    # Dependency management___________________
    def test_can_register_function(self, manager: Manager):
        function = None
        # This registers the function with its generated name automatically (alternatively you can also specify the name directly)
        manager._orchestrator.register(function)
        assert manager._orchestrator._functions[function.name] == function, "must register the function internally within its state"

    # You can schedule/register a function in the system
    def test_can_schedule_function(self, manager: Manager):
        function = None
        # This registers the function with its generated name automatically (alternatively you can also specify the name directly)
        manager._orchestrator.schedule(function, '5 * * * *')
        assert manager._orchestrator._functions[function.uid] == function, "must register the function internally within orchestrator state"

    def test_can_access_registered_function(self, manager: Manager):
        function = None
        manager._orchestrator.schedule(function)
        function = manager._orchestrator.get(function.uid)

    def test_can_add_dependence(self, manager: Manager):
        function = None
        function2 = None
        func_obj = manager._orchestrator.register(function)
        func_obj.depends_on(function2)

        assert manager._orchestrator.head() == function2, "upstream dependency must take head"
        assert manager._orchestrator.head().next() == func_obj, "function registering the upstream must be set `next` to upstream dependency"

    def test_can_set_trigger(self, manager: Manager):
        function = None
        function2 = None
        func_obj = manager._orchestrator.register(function)
        func_obj.triggers(function2)

        assert manager._orchestrator.head() == function, "function registering trigger must be the head node"
        assert manager._orchestrator.head().next() == function2, "function being triggerd must be a child to the triggering function"
    
    def test_can_set_conditional_trigger(self, manager: Manager):
        function = None
        function2 = None
        func_obj = manager._orchestrator.register(function)
        func_obj.triggers(function2, on=['Success', 'Skipped'])
        
        assert manager._orchestrator.head() == function, "function registering trigger must be the head node"
        assert manager._orchestrator.head().next() == function2, "function being triggerd must be a child to the triggering function"
        #TODO Define how the trigger conditions are represented in the orchestrator state, and in the backend and test for it

    def test_can_iterate_over_param(self, manager: Manager):
        function = None
        function2 = None
        func_obj = manager._orchestrator.register(function)
        iterator_node = func_obj.iterates_over('param1')
        assert isinstance(manager._orchestrator.head(), IteratorNode)
        assert iterator_node.function == function, "The iterator node must relate the executable function within its state"
        assert False, "Iterator must list the parameters to iterate over"
        assert False, "Iterator must contain the iteration type per parameter"


    def can_track_dependencies(self, orchestrator):
        """Can create a dependency graph in which executable objects can be scheduled in their interaction"""
        function = None # Get an executable object to schedule from the compiler
        function1 = None # Get an executable object to schedule from the compiler
        function2 = None # Get an executable object to schedule from the compiler
        function3 = None # Get an executable object to schedule from the compiler
        
        # All methods that register a function without a further upstream dependency return a execution_graph object that exposes the API to the orchestrator component
        # func_obj = orchestrator.schedule(function, schedule)
        func_obj = orchestrator.register(function)
        # Describes a parameter resolution dependency function gets resolved outputs from (function1, function2)
        # orchestrator.register(function).uses_resolved_param('parm1', function1).uses_resolved_param('param2', function2) # Both param1, param2 are linked to schedule only, no lineage amongst themselves

        # Methods on the function object returned from registering a function/or scheduling it provide an interface to chain dependencies
        # func_obj.resolves('paramname') # Indicate a function resolves a parameter (High level abstraction to coordinate dependencies)
        func_obj.depends_on('functionname') # Indicate a dependency lineage 
        func_obj.triggers('functionname', on=['Success', 'Skipped']) # The function triggers the other function on 'ExitStatus ('Success' and 'Skipped')
        func_obj.iterates_over('param_in_function')
        # But you can also access all functions from the orchestrator


    # Executive capacities____________________
    def test_can_schedule_a_function(self, manager: Manager):
        """Schedule a function with the """
        pass

