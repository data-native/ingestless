"""


"""
from restmap.templateParser.TemplateParser import TemplateSchema
from restmap.resolver.ResolutionGraph import ResolutionGraph
class Resolver:
    """
    
    """

    def __init__(self) -> None:
        pass
    
    def resolve(self, template: TemplateSchema) -> ResolutionGraph:
        """
        Generate a resolved graph representation of the dependency
        parse tree. 

        The resolution creates:
        * An entry for each execution step
        * Looping contracts holding a compute step and associated attributes
        * Resolver nodes that when executed will read and provide a certain attribute
        """
        # Add all resolvers

        # Add all parameters
        
        # Add all endpoints utilizing the resolver and parameter node references

        # 
        raise NotImplementedError
    


    