from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode 

from typing import Optional
@dataclass
class ResponseHandlerBase:
    pass

@dataclass
class ResponseHandlerDefaults:
    success_code: int = 200
    error_code: int = 500
    return_type: str = 'json'
    return_variable: str = 'body'
    dlq: str = None
    
@dataclass
class ResponseHandlerNode(ResponseHandlerDefaults, CompilerNode , ResponseHandlerBase):
    """
    Handles the compilation of response handler logic
    
    * Enable to set the body result param to pass back
    * Enable to set validation
    """

    def compile_code(self):
        """
        Extract parameters for the compilation from the 
        """
        param_dict = {
            'response_check': self._compile_response_check(),
            'success_code': self.success_code,
            'error_code': self.error_code,
            'return_type': self.return_type,
            # Implement a DLQ catch for failing executions
        }

        return self._render_template(param_dict)

    def _compile_response_check(self) -> Optional[str]:
        """
        Create assertions to guard the response creation.
        @return: None or code string
        """
        return None

    
        