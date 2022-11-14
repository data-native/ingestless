"""

"""

class Node:

    def __init__(self) -> None:
        pass

class Endpoint(Node):
    """
    Represents a logical REST endpoint in the computation
    graph. Parametrization on this node can either be hardcoded, 
    or provided through a resolver instance.
    """

    def __init__(self) -> None:
        
        super().__init__()
    

class ResolutionGraph:
    """
    The parse graph represents the logical
    dependency resolution amongst the scheduled
    assets in a given endpoint workflow.
    """

    def __init__(self) -> None:
        pass
    
    def add_endpoint(self, endpoint: dict):
        raise NotImplementedError
    
    def add_resolver(self, resolver: dict):
        raise NotImplementedError
    
    def add_parameter(self, param: dict):
        raise NotImplementedError
    
    def __repr__(self) -> str:
        #TODO: Represent in tabular format
        return "Resolution Graph" 
    

    