import pytest

from restmap.manager.State import State

@pytest.fixture()
def clean_state():
    state = State()
    return state

@pytest.fixture()
def set_state():
    state = State()
    #TODO: Define state update
    update = {}
    state._update_schema(update)
    return state


@pytest.fixture()
def state_update():
    return {
       #TODO: Define the state update 
    }

@pytest.fixture()
def state_removal():
    return {
        #TODO: Define a smaller state, deleting from state_update
    }

def test__initalize_backend(clean_state: State):
    clean_state._initialize_backend() 
    assert False, "should define a state dictionary with version 0"
    assert False, "should initialize a remote state backend if initialized"

def test__compile_state_diff(clean_state: State, set_state: State,  state_update: dict, state_removal: dict):
    # Compare against empty state
    assert clean_state._compile_state_diff(state_update), "should accept state_update in full as incremental update"
    assert set_state._compile_state_diff(state_removal), "should accept state removal in full"
    assert set_state._compile_state_diff(state_update), "should identify identity between the two states"

def test_validate(clean_state: State):
    assert clean_state

def test_current_version(clean_state: State, set_state: State, state_removal, state_update):
    assert clean_state.current_version == 0, "fresh state should have version 0"
    assert set_state.current_version == 1, "with a single update version should be 1"
    set_state._update_schema(state_removal)
    assert set_state.current_version == 2, "a removal should count as a new version increase by 1"
    set_state._update_schema(state_update)
    assert set_state.current_version == 3, "an addition should count as a new version increase by 1"

def test__add(clean_state: State):
    #TODO: Define endpoint instance to add to schema
    endpoint = {}
    actual_version = clean_state.current_version
    clean_state._add(endpoint)
    assert endpoint.name in clean_state._components, "Component should be registered by name in state.components"
    assert clean_state.current_version == actual_version, "Internal activity to add an element should not increase version by itself. Should be acting as a transaction"

def test__remove(set_state: State): 
    #TODO: Set the component to one included in the update to clean_state
    component = None
    actual_version = set_state.current_version
    set_state._remove(component)
    assert component.name not in set_state._components, "Component should no longer be registered with the component state"
    assert set_state.current_version == actual_version, "Internal activity to remove element should not increase version by itself. Should be acting as a transaction"

def test__get(set_state: State):
    #TODO: Set the name of a component registered to set_state
    component = None
    retrieves = set_state._get(component)
    #TODO: Replace string check with correct return type
    assert isinstance(retrieves, str), "Should be a component instance"

     

    

    

    
