"""
A potential collection for all compilation steps around code
generation
"""
from typing import Union, List, Dict, Optional
from dataclasses import dataclass

@dataclass 
class CompilerNode:
    parent: 'CompilerNode'
    children: List['CompilerNode']
    code: str = ""

    def add_child(self, node: 'CompilerNode'):
        self.children.append(node)
    
    def compile(self):
        return self.code

@dataclass
class HeaderNode(CompilerNode):
    pass

@dataclass
class HandlerNode(CompilerNode):
    pass
@dataclass
class RequestNode(CompilerNode):
    pass

@dataclass
class BodyParserNode(CompilerNode):
    pass

class BaseCompiler:
    def __init__(self) -> None:
        self.head = CompilerNode(None, [])
class PythonCompiler(BaseCompiler):
    """
    Compiles business logic
    
    * Compile header
    * Compile 
    """
    def __init__(self) -> None:
        super().__init__()
    
    def header(self):
        header = HeaderNode(self.head, [])
        self.head.add_child(header)
        return header
         
    def request_handler(self):

        raise NotImplementedError
    
    def body_validation(self):
        raise NotImplementedError


    def compile(self):
        pass