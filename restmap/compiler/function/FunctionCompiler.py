"""
Compiler
------------
* Use a graph to create nested elements as 

"""
from typing import Union, List, Dict, Optional
from dataclasses import dataclass

from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.compiler.function import HandlerNode, HeaderNode, RequestNode, BodyParserNode
from restmap.compiler.BaseCompiler import BaseCompiler
from restmap.compiler.CompilerNode import CompilerNode
from restmap.compiler.function.AuthenticatorNode import AuthenticatorNode
from restmap.compiler.function.ResponseHandlerNode import ResponseHandlerNode


# FUNCTION_COMPILER__________________________
@dataclass 
class FunctionCompilationRequest:
    """
    A resolution graph nested subgraph specifying 
    an executable function.
    
    It has to be extracted from the ResolutionGraph and 
    passed to the Function Constrcut Compiler class for compilation.
    """
    url_generator: str
    authentication: str

    
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
    def __init__(self, compilation_dir: str='./ingestless/restmap/src', language:str="Python@3.9") -> None:
        super().__init__(compilation_dir)

    def compile(self, head: CompilerNode, function: ResolutionGraph) -> DeployableFunction:
        """
        Assumes a loaded resolution graph that was transformed into the compilation graph

        * Loads the asssociated function template
        * Compiles the compilation graph into the code file
        * Parametrizes the deployment configuration for deployment through the backend provider
        
        return: Function object that can be deployed through the backend provider
        """
        # TODO Elaborate the validation logic to handle optional or missing elements in the construct definition
        expected_nodes = [HeaderNode.HeaderNode, HandlerNode.HandlerNode, BodyParserNode.BodyParserNode, ResponseHandlerNode]
        assert all([node in head._children] for node in expected_nodes)

        code = ""
        # TODO Resolve the graph for all functions
        # TODO Handle the fact if not all elements are valid
        code += self._compile_header(head, function)
        code += self._compile_request(head, function)
        code += self._compile_body(head, function)
        code += self._compile_response(head, function) 

        # Passes the completed compilation graph to a specific compiler plugin
        # allowing specific languages and framework combinations to implement the 
        # compilation to code based on the same overall resolved compilation attributes
        # that are passed to them at this point
        # Render code template
        requirements = self._compile_requirements(head)
        deployment_params = self._compile_params()

        return DeployableFunction(
            code=code,
            runtime="Python@3.9",
            requirements= requirements,
            params = deployment_params
        )

    def _compile_header(self, parent: CompilerNode, graph: ResolutionGraph) -> str:
        """
        Extracts required attributes from ResolutionGraph and 
        instantiates the HeaderNode.

        Conditional structure
        ----------------------
        * Authentication: 
        * HTTP/HTTPS:
        * 
        """
        header_params = None
        # Extract all data from graph
        # Instantiate the node
        header = self.header(parent=parent)
        # Conditionally append authenticator
        return header.compile_code()

    def _compile_request(self, parent: CompilerNode, graph: ResolutionGraph) -> str:
        """
        Compiles the request to be executed against the target endpoint
        """
        request = self.request(parent=parent)
        # Generate all elements to be nested in the request object based on set parameters

        # Compile the configured request handler to code and return code string
        return request.compile_code()
        
    def _compile_response(self, parent: CompilerNode, graph: ResolutionGraph) -> str:
        """
        Compiles the code handling the response object generation
        from the serverless function
        """
        response = self.response_handler(parent=parent)
        # Attribute to the reponse object based on set parameters on the graph
        
        return response.compile_code()

    def _compile_body(self, parent: CompilerNode, graph: ResolutionGraph) -> str:
        """
        Compiles the code logic to handle the core logic in the function
        
        This contains the main application logic provided by a library of plugins.
        Based on available parameters of the function for standard procedures, 
        or through `custom code components` that contain an executable to be
        automatically executed in the function body.
        """
        body = self.body_parser(parent=parent)
        # Attribute the list of associated plugins based on attributes on the graph

        # Compile code
        return body.compile_code()

    def _compile_requirements(self, head: CompilerNode):
        """
        Compiles the list of requirements for the function to be executable
        """
        return {}

    def header(self, 
        parent: CompilerNode,
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
            _parent=None,
            _children=[]
            )
        self._append_to_parent(parent, header)
        return header
         
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
        return DeploymentParams(
            min_allocated_memory_gb=128,
            max_allocated_memory_gb=256,
            timeout=300,
            permissions=['DynamoDBReader'],
            env_variables={},
            tags=[],
            is_monitored=True,
            is_traced=True,
            concurrency=10
        )
    # TODO: Remove and replace with build in jinja function
    
    #TODO
    def request(self, 
        parent: CompilerNode, 
        template: str="functions/aws/",
        ) -> HandlerNode.HandlerNode:
        """
        Create the compiled handler Node
        """
        handler = HandlerNode.HandlerNode(
                _template=template, 
                _env=self.env, 
                _parent=None, 
                _children=[], 
                code='Handler Code\n')
        self._append_to_parent(parent, handler)
        return handler
    
    def body_parser(self, 
        parent: CompilerNode,
        template:str="functions/aws/body_parser.jinja",
        ) -> BodyParserNode.BodyParserNode:
        parser = BodyParserNode.BodyParserNode(
            _template=template,
            _env=self.env, 
            _parent=None,
            _children=[]
            )
        self._append_to_parent(parent, parser)
        return parser

    def response_handler(self,
        parent: CompilerNode, 
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
            _parent=None, 
            _children=[]
        )
        self._append_to_parent(parent, response_handler)
        return response_handler
    
    def authenticator(self,
        parent: CompilerNode,
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
            _parent=None,
            _children=[]
        )
        self._append_to_parent(parent, authenticator)
        return authenticator
        

    def _save_to_file(self, name:str, doc: str):
        """Output the compilation result to file location"""
        self.output_location.mkdir()
        path = self.output_location / f"{name.split('.')[0]}.py" 
        path.write_text(doc) 


    def _append_to_parent(self, parent: CompilerNode, node: CompilerNode):
        """Appends to given parent, or else to Compilation Tree root"""
        parent.child(node) 


