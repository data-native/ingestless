"""
Compiler
------------
* Use a graph to create nested elements as 

"""
from typing import Union, List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape

from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.compiler import HandlerNode, HeaderNode, RequestNode, BodyParserNode

@dataclass 
class CompilerNode:
    parent: 'CompilerNode'
    children: List['CompilerNode']
    code: str = ""
    is_enclosing: bool = False

    def add_child(self, node: 'CompilerNode'):
        self.children.append(node)

    def add_sibbling(self, node: 'CompilerNode'):
        self.parent.add_child(node)
    
    def compile(self):
        """
        Traverse the generated compilation tree and resolve each element
        given its own parameters and the neighborhoud of its parent and
        children.

        #TODO: Update to 'compile' each nested structure up to its 'enclosing elements' which 
        * A node containing embedded children, should resolve them and return a total value
        * 
        """
        if self.is_enclosing:
            # Needs to first compile its children before it can return its final string
            # Iterates over all 
            self._compile_enclosed_nodes()
         
        # Then 
        current_node = self.head
        while current_node:
            if current_node == self.head and not current_node.children:
                # break out when reaching the root node
                return
            if not current_node.children:
                # Reached a leave
                current_node.compile()
                # Remove the child from the parent
                current_node.parent.children = [node for node in current_node.parent.children if node != current_node]
                # go a level up
                current_node = current_node.parent
            else:
                current_node = current_node.children[0]
        else:
            # Doesn't have any children of its own and 
            pass

    def _compile_enclosed_nodes(self):
        pass


class BaseCompiler:
    def __init__(self, compilation_dir:str='./ingestless/restmap/src') -> None:
        self.head = CompilerNode(None, [])
        self.env = Environment(loader=PackageLoader("restmap", "compiler/templates"), autoescape=select_autoescape())
        self.output_location = Path(compilation_dir)
    
class PythonCompiler(BaseCompiler):
    """
    Compiles business logic
     
    Can add elements to the graph.
    Can iterate over the parse tree and compile the code.
    Tree structure allows the nodes to take their context
    into account.
    """
    def __init__(self) -> None:
        super().__init__()
    
    def header(self):
        header = HeaderNode(self.head, [], 'Header Code\n')
        self.head.add_child(header)
        return header
         
    def handler(self):
        handler = HandlerNode(self.head, [], 'Handler Code\n')
        self.head.add_child(handler)
        return handler
    
    def body_parser(self):
        parser = BodyParserNode(self.head, [], 'Parser Code\n')
        self.head.add_child(parser)
        return parser
    
    def from_resolution_graph(self, graph: ResolutionGraph)

        
    def compile(self):
        """
        This assumes that the code component have been compiled
        """
        # Compile the components
        self._compile_code_components()
        #Load the template
        template_name = "aws_lambda_python.jinja"
        template = self.env.get_template(template_name)
        rendered_template = template.render(package_imports="from manager import test", dependent_functions="Dependents", documentation_strin="test doc string", return_statement="'A string return'")
        self._save_to_file(template_name, rendered_template)
        return rendered_template

    def _save_to_file(self, name:str, doc: str):
        """Output the compilation result to file location"""
        self.output_location.mkdir()
        path = self.output_location / f"{name.split('.')[0]}.py" 
        path.write_text(doc) 