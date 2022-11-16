"""

"""
from dataclasses import dataclass

@dataclass
class IaCTemplate:
    """
    Abstracts an infrastructure automation output
    across multiple backend provider. 

    First implemented for Terraform
    """
    pass

@dataclass
class TerraformTemplate(IaCTemplate):
    """
    Terraform compilation output format 
    """
    pass

class Compiler:
    """
    Receives a ResolutionGraph and a backend provider
    and compiles it into a IaC template for infrastructure
    automation and code generation for integration logic
    """
    
    def compile(self, graph: ResolutionGraph) -> IaCTemplate:
        """
        
        """