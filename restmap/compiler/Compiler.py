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
        self.code = ''
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
         
    def handler(self):
        handler = HandlerNode(self.head, [])
        self.head.add_child(handler)
        return handler
    
    def body_parser(self):
        parser = BodyParserNode(self.head, [])
        self.head.add_child(parser)
        return parser

    def compile(self):
        current_node = self.head
        while current_node:
            if not current_node.parent:
                return
            if not current_node.children:
                # Reach a leave
                self.code + current_node.compile()
                # Remove the child from the parent
                current_node.parent.children = [node for node in current_node.parent.children if node != current_node]
                # go a level up
                current_node = current_node.parent()
            else:
                current_node = current_node.children[0]