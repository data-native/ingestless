"""
State Manager class
"""

class State:
    """
    Provides the management API to the application state
    """

    def __init__(self) -> None:
        self._state = {}
        self._components = {}
    
    def _initialize_backend(self):
        """
        Deploys and configures the state backend storage
        """
        raise NotImplementedError
    
    def _compile_state_diff(self, update):
        """
        Compiles the difference between the current local state
        and the recorded backend state in the application.

        Initially only compares template versions kept in state
        and not the actual state of the backend.
        """
        raise NotImplementedError

    def _update_schema(self, update) -> None:
        """
        Updates the local state based on the update object
        Keeps a versioned history of state changes.
        """
        # Ensure there is a difference
        diff = self._compile_state_diff(update)
        if diff:
            curr_version = 0
            # store as bumped up state version
            
            #TODO: Store the differences and implement a replay functionality to roll back/forward the changes
            self._state[curr_version + 1] = diff

    def roll_back(self, version: int):
        """
        Reverts the current state back to a previously saved version
        """
        # Ensure version in state versions
        if not version < self._state.current_version():
            raise ValueError("Version is higher than current version {self._state.current_version()}")

    @property
    def current_version(self):
        return max(self._state.keys())


    def _add(self, component) -> None:
        """
        Adds a given component to the state management
        """
        raise NotImplementedError

    def _remove(self, component):
        """
        Removes a given component from state management
        """
        # Remove it from local state cleaning up all dependencies
        
        # Undeploy it 
        raise NotImplementedError
    
    def _get(self, component) -> AnyString:
        """
        Retrieves a given component from the state
        """


    def _list_components(self):
        """
        Returns the list of maintained components
        """
        raise NotImplementedError

    def _persist(self):
        """
        Persist the current state to the backend
        """
        raise NotImplementedError
    
    def _load(self):
        """
        Retrieves state from the backend storage location
        """
        raise NotImplementedError
