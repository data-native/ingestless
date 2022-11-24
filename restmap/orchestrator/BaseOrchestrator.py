"""

"""

class BaseOrchestrator:
    """
    The orchestrator schedules the execution of functions, 
    maintains their dependencies across runs and ensures
    that outputs from a function can be channeled to the 
    dependent functions to allow features such as parameter
    resolution from EndpointResolver without an intermediary
    storage system.
    
    # TODO Can schedule a function to execute after another
    # TODO Can execute a function iteratively 
    # TODO Can pass the output of a function as input to the next
    # TODO Can retry a function if it fails

    """
    
    def ___init__(self):
        pass

    def schedule(self, function):
        """
        Schedule a regular execution of a function
        """
        raise NotImplementedError

    def (self, function):
        """
        
        """
        raise NotImplementedError

    def schedule(self, function):
        raise NotImplementedError

    def schedule(self, function):
        raise NotImplementedError