
class BaseNode:
    """
    A graph node within the ResolutionGraph is instantiated
    with parameters received from the configuration template.
    It can carry flexible parameters as either params or resolver
    functions which need to be resolved on execution. 

    The Node acts as an intermediary representation that can be scheduled
    and eventually be compiled onto a specific backend implementation
    using backend providers.
    """

    def __init__(self) -> None:
        pass

    def compile(self, provider):
        """
        Called on each node when the graph gets executed
        """
        # Should generate a provider specific representation of 
        raise NotImplementedError
    


    