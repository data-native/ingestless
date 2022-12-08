from typing import Dict
from dataclasses import dataclass, field
from restmap.compiler.CompilerNode import CompilerNode
from restmap.enums import RestMethod

@dataclass
class RequestHandlerNodeBase:
    method: str
    response_type: str
    response_variable: str
    response_status: str

@dataclass
class RequestHandlerNodeDefaults:
    request_body: dict = field(default_factory=dict) 
    timeout: int = 500
    retry: int = 3

@dataclass
class RequestHandlerNode(RequestHandlerNodeDefaults, CompilerNode, RequestHandlerNodeBase):
    """
    Compiles the request handler configuration for function integration
    
    * All parameters are defined on the class init so they are clearly communicated and enforced
    * The def compile_code compiles the parametrization into the template
    *  
    """

    def _assert_valid_config(self):
        # Ensure correct configuration according to the RestMethods
        if self.method == 'GET':
            # self.body is optional
            pass
        elif self.method == 'POST':
            assert self.request_body, "For POST a payload must be configured"
        # TODO Extend with all parameter configuration checks required 

    # TODO Add method interfaces to allow the parametrization of the node

