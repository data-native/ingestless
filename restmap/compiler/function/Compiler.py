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
from restmap.compiler.CompilerNode import CompilerNode
from restmap.compiler.AuthenticatorNode import AuthenticatorNode
from restmap.compiler.ResponseHandlerNode import ResponseHandlerNode

class BaseCompiler:
    def __init__(self, compilation_dir:str='./ingestless/restmap/src') -> None:
        env = Environment(loader=PackageLoader("restmap", "compiler/templates"), autoescape=select_autoescape())
        self.env = env 
        self.head = CompilerNode(
            _env=env, 
            _template=None, 
            _parent=None, 
            _children=[])
        self.output_location = Path(compilation_dir)
# TODO: Generalize the compiler to accept a language parameter and load the templates accordingly

# FUNCTION_COMPILER__________________________
@dataclass
class DeploymentParams:
    """
    Standard set of parameters to configure the deployment
    of the serverless function on the BackendProvider

    Represents the function service contract to be implemented
    by the Backend Provider
    #TODO Implement the receiving interface on the base backend provider
    """
    min_allocated_memory_gb: int
    max_allocated_memory_gb: int
    timeout: int
    permissions: List[str]
    env_variables: dict
    tags: List[str]
    is_monitored: bool
    is_traced: bool
    concurrency: int

@dataclass
class FunctionRequirement:
    """
    Defines a package requirement
    """
    library: str
    version: str
    imports: List[str]

@dataclass
class DeployableFunction:
    """
    The compilation output that can be send to the 
    BackendProvider for function deployment
    
    Defines the contract between `Compiler` and `BackendProvider`
    """
    code : str
    runtime: str 
    requirements: List[FunctionRequirement] 
    params: DeploymentParams

class FunctionCompiler(BaseCompiler):
    """
    Compiles business logic
     
    Can add elements to the graph.
    Can iterate over the parse tree and compile the code.
    Tree structure allows the nodes to take their context
    into account when creating code fragments.
    """
    def __init__(self, compilation_dir: str='./ingestless/restmap/src') -> None:
        super().__init__(compilation_dir)

    # Rename to 'from_ 
    def from_resolution_graph(self, graph: ResolutionGraph):
        """
        Parses the resolution graph into the compilation graph
        
        * Each functional component is compiled based on template parameters
        * Each section is represented as a potentially nested subtree
        * Each subtree section is defined by 'enclosing CompilerNodes'
        * Each 'enclosing node' contains a nested structure of all elements it requires to parametrize its section
        """
        # TODO Resolve the graph for all functions
        
        # Set up all nodes to configure the compilation
        header = self.header()
        handler = self.handler()
        parser = self.body_parser()

        # Add nested elements to the function structure based on template parametrization
        # TODO: Move the iteration over the endpoints out of here into BaseCompiler and add FunctionCompiler in a list of compilers registered there to handle compilation of all supported types
        for endpoint in graph._endpoints:
            # Compile header based on configuration
            `21k`

    def header(self, 
        authentication: str = None,
        template:str="functions/aws/header.jinja",
    ) -> HeaderNode.HeaderNode:
        """
        Compiles the HTTP header code

        * HTTP / HTTPS
        * Authentication protocolls (Token passing)
        * CORS Settings
        * #TODO Extend list of supported header configurations here .....
        """
        header = HeaderNode.HeaderNode(
            _template=template,
            _env=self.env,
            _parent=self.head,
            _children=[]
            )
        self._append_to_parent(header)
        # Handle Authentication
        if authentication:
            header.child(self.authenticator())

        return header
         
    #TODO
    def handler(self, template: str="functions/aws/") -> HandlerNode.HandlerNode:
        """
        Create the compiled handler Node
        """
        handler = HandlerNode.HandlerNode(
                _template=template, 
                _env=self.env, 
                _parent=self.head, 
                _children=[], 
                code='Handler Code\n')
        self._append_to_parent(handler)
        return handler
    
    def body_parser(self, template:str="functions/aws/body_parser.jinja") -> BodyParserNode.BodyParserNode:
        parser = BodyParserNode.BodyParserNode(
            _template=template,
            _env=self.env, 
            _parent=self.head, 
            _children=[]
            )
        self._append_to_parent(parser)
        return parser

    def response_handler(self, 
        template:str="functions/aws/response_handler.jinja",
        parse_to: str = 'json',
        escape_strings: bool = False,

        ):
        """
        Parametrizes and appends a ResponseHandler Node to the compilation graph.

        Response generation and handling 
        """
        response_handler = ResponseHandlerNode(
            _template=template,
            _env=self.env, 
            _parent=self.head, 
            _children=[]
        )
        self._append_to_parent(response_handler)
        return response_handler
    
    def authenticator(self,
        parent: CompilerNode = None,
        template:str="functions/aws/authenticator.jinja",
    ) -> AuthenticatorNode:
        """
        Parametrizes and appends an authenticator to the given parent node

        Authentication methods supported
        --------------------------------
        Basic Auth:
        API Key:
        OAuth 2.0:
        OpenIDConnect:
        """
        authenticator = AuthenticatorNode(
            _template=template,
            _env=self.env,
            _parent=self.head,
            _children=[]
        )
        
        self._append_to_parent(authenticator)
        
    def compile(self) -> DeployableFunction:
        """
        Assumes a loaded resolution graph that was transformed into the compilation graph

        * Loads the asssociated function template
        * Compiles the compilation graph into the code file
        * Parametrizes the deployment configuration for deployment through the backend provider
        
        return: Function object that can be deployed through the backend provider
        """
        #Load the template
        template_name = "aws_lambda_python.jinja"
        template = self.env.get_template(template_name)
        # Render code template
        code = template.render(package_imports="from manager import test", dependent_functions="Dependents", documentation_strin="test doc string", return_statement="'A string return'")
        requirements = self._compile_requirements()
        deployment_params = self._compile_params()
        #TODO: Replace with native jinja functionality
        self._save_to_file(template_name, code)
        #TODO Define parameters based on semantics for the 'generlized function' service to be deployed by the BackendProvider

        return  DeployableFunction(
            code=code,
            runtime="Python@3.9",
            requirements= requirements,
            params = deployment_params
        )

    def _compile_params(self) -> DeploymentParams:
        """
        Compiles the deployment parameters for the function
        given the overall configuration of the elements of the
        function code. 

        Caluclated params
        ----------------------
        * Allocated memory
        * Parallelism
        * 
        """
        return DeploymentParams()
    # TODO: Remove and replace with build in jinja function
    
    
    def _save_to_file(self, name:str, doc: str):
        """Output the compilation result to file location"""
        self.output_location.mkdir()
        path = self.output_location / f"{name.split('.')[0]}.py" 
        path.write_text(doc) 

    def _compile_requiements(self) -> List[FunctionRequirement]:
        """
        Generates the list of imports required for the given code file
        """

    def _append_to_parent(self, parent: CompilerNode, node: CompilerNode):
        """Appends to given parent, or else to Compilation Tree root"""
        parent = parent if parent else self.head
        parent.child(node) 

