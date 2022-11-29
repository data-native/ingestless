from abc import ABC, abstractclassmethod, abstractstaticmethod, abstractproperty, abstractmethod
from typing import List, Union
from restmap.compiler.function.FunctionCompiler import FunctionDeployment

class AbstractFunctionProvider(ABC):
    """
    TO BE IMPLEMENTED
    """
    # TODO Provide implementation 
    @abstractmethod
    def register(self, function: Union[FunctionDeployment, List[FunctionDeployment]]) -> List['FunctionProvider']:
        """
        Register one or more functions based on their specification
        """

    @abstractmethod
    def compile(self, function: FunctionDeployment) -> 'AbstractFunctionProvider':
        """
        Creates a AWS Lambda based on the FunctionDeployment configuration
        """
    
    @abstractmethod
    def use_function(self, function: str) -> 'AbstractFunctionProvider':
        """
        """
    
    @abstractmethod
    def withRole(self, role:str) -> 'AbstractFunctionProvider':
        """
        Assigns a role to the function
        Works against the active function construct
        """

    @abstractmethod
    def triggers(self, target, params: dict):
        """
        Chains the given functions execution to the previous
        execution of the other function. 

        Can optionally set the list of execution outcome statuses
        to trigger on. By default only triggers on successful execution.
        """