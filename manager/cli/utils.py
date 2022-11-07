"""
Utility functions specifically for the CLI component
"""
from typing import List

def get_argument_list(input:str, type:type = int) -> List:
    """
    Extracts a list of arguments from a string input. 

    Handles the extraction of arguments from separation chars and strips
    whitespace around arguments. 
    @type: defines which type the input should be parsed as
    """
    if len(input) == 1:
        argument_list = [exec("type(input)")]
    else:
        argument_list = [int(i.strip()) for i in input.replace(';', ' ').split(' ')]     
    
    return argument_list
 