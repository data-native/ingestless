"""
State Manager class
"""
from enums import StatusCode
from dataclasses import dataclass, field

from restmap.templateParser.TemplateParser import TemplateSchema

@dataclass
class ComponentDict:
    """
    Stores the registered components at a specific point
    in time     
    """
    components: dict = field(default_factory=dict)
     
@dataclass
class StateDict:
    """
    Manages a changelog of application states
    with the abbility to revert or replay changes
    incrementally to recreate the state at any point
    in time.
    """
    components: ComponentDict
    state: dict = field(default_factory=dict)

    @classmethod
    def from_template(cls, template: TemplateSchema) -> 'StateDict':
        
        components = {}
        component_dict = ComponentDict(components)
        state = {}
        return StateDict(components=component_dict, state=state)

    def get_diff(self, other: 'StateDict'):
        """
        Compute the difference between the current and other state
        dict in terms of additions and removals
        """
        # Check if identical and if return early

        # Compute set difference

        # Compute removals

        # Compute additions

        # return removals, additions
        raise NotImplementedError
    

class State:
    """
    Provides the management API to the application state
    """

    def __init__(self) -> None:
        self._state: dict[int, StateDict] = {}
        self._current_version: int = 0
    
    @property
    def components(self):
        return self._state[self.version].components

    @property
    def version(self):
        return self._current_version  

    @version.setter
    def version(self, version: int):
        if version <= self.version:
            raise ValueError("Version number is already used")
        self._current_version = version
    
    @property
    def state(self) -> StateDict:
        return self._state[self._current_version]
    @state.setter
    def state(self, update: TemplateSchema) -> StatusCode:
        # Check that StateDict is valid
        updated_state = StateDict.from_template(update)
        # Compile to 
        diff = self.state.get_diff(updated_state)
        if not diff:
            return StatusCode.FILE_ERROR

        self._state[self.version + 1] = updated_state
        return StatusCode.SUCCESS

    def describe(self):
        """
        Represent the current state
        """
        #TODO: Return a formated string representation
        return self.state
    
    def roll_back(self, version: int) -> StatusCode:
        """
        Reverts the current state back to a previously saved version
        """
        # Ensure version in state versions
        if not version < self.version:
            raise ValueError("Version is higher than current version {self._state.current_version()}")

        # Update the version tracking to new version
        self.version = version
        # TODO: Ensure old state is applied correctly
        return StatusCode.SUCCESS

    def _initialize_backend(self):
        """
        Deploys and configures the state backend storage
        """
        # Ensure backend configuration is present
        
        # Deploy backend resources

        # Initialize backend storage
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
