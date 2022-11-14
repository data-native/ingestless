from dataclasses import dataclass
from .BaseNode import BaseNode
from .ParamNode import ParamNode

@dataclass
class EndpointNode(BaseNode):
    """
    Represents an endpoint in the computation graph 
    """
    base_url: str
    params: list[ParamNode]

    def compile(self, provider):
        pass

    def _compile_url(self):
        """
        Dynamically generate the url based on available
        parameters
        """
    
