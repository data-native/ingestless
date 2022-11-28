"""
Implmements an AWS native Orchestrator

Services used:
--------------
* EventGrid Scheduler
"""
from restmap.executor.BaseProvider import BaseBackendProvider
from .BaseOrchestrator import BaseOrchestrator

class EventGridOrchestrator(BaseOrchestrator):
    """
    
    """
    
    def __init__(self, provider: BaseBackendProvider) -> None:
        super().__init__()
        self._provider = provider

    def schedule(self, function):
        pass