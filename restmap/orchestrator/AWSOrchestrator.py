"""
Implmements an AWS native Orchestrator

Services used:
--------------
* EventGrid Scheduler
"""
from .BaseOrchestrator import BaseOrchestrator

class EventGridOrchestrator(BaseOrchestrator):
    """
    
    """

    def schedule(self, function):
        pass