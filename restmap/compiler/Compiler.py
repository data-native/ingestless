"""
A potential collection for all compilation steps around code
generation
"""

class BaseCompiler:
    def __init__(self) -> None:
        pass

class PythonCompiler(BaseCompiler):
    """
    Compiles business logic
    """
    
    def __init__(self) -> None:
        super().__init__()