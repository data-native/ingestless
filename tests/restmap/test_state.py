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
    assert clean_state.version, "should define a state dictionary with version 0"
    assert False, "should initialize a remote state backend if initialized"

def test_version(clean_state: State, set_state: State, state_removal, state_update):
    assert clean_state.version == 0, "fresh state should have version 0"
    assert set_state.version == 1, "with a single update version should be 1"
    set_state = state_removal
    assert set_state.version == 2, "a removal should count as a new version increase by 1"
    set_state = state_update
    assert set_state.version == 3, "an addition should count as a new version increase by 1"

     

    

    

    
