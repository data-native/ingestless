"""
The Compiler generates a set of parametrized deployable construct
definition instances to be further orchestrated and deployed onto a given target infrastructure.

The compiler contains the definition of the parameters to be set on 
any type of supported deployable construct such as a serverless function, queue, table, etc.

Compilation sets the construct deployment parameter for a given construct based on the 
nested structure of components the construct is configured with in the template definition.
The contextual analysis enables the Compiler to apply optimization both on the level of code
generation, but also on the service parametrization level. 

## Code compilation
The received ResolutionGraph contains either flat, or nested construct definitions whereby
the nested case provides a set of independently parametrized sub components that require a 
joint compilation to generate the target code. 

As an example, the parsing stage of the response body received from a REST request can contain
one or multiple required transformations based on the given response format and target
output format for the function. 

The definition would look something like
```python
parser = resolver.bodyParser()
parser.parse_incoming('JSON')
parser.return_variable('data')
parser.return_format('parquet')
```
The compilation of the code associated now creates a linear set of transformation
steps resulting in a `data` variable holding parquet transformed JSON response data.

The compiler handles each step in the nested logic as a compilable Node instance that
is analyzed both in terms of the parameters set on it, as well as its position in the logic.
Determining this context, the Compiler can make informed decisions on code optimization.

## Parametrization
Each supported `serverless construct` provides an abstraction from the platform specific implementation on a given
public cloud or native stack. The Compiler houses the logic of parametrizing the specified
`DeployableConstruct` class interfaces that provide this serverless abstraction semantics. 

The Compiler receives the resolved configuration tree and the code compilation output and uses
this information to infer optimal settings for all involved constructs. The actual generation
of the serverless assets does not happen here, but after orchestration in the `Orchestrator` component.

## Construct specific Compilers
The main Compiler class deferrs the compilation logic for a given construct onto
`Construct Compiler plug-ins` and communicates its requirements through a set of
request data objecs called `CompilationRequest`


"""
# TODO Add Doc on communication between compiler and construct compiler
from typing import Union, List, Dict, Optional
from pathlib import Path
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
class FunctionDeployment:
    """
    The compilation output that can be send to the 
    BackendProvider for function deployment
    
    Defines the contract between `Compiler` and `BackendProvider`
    """
    code : str
    runtime: str 
    requirements: List[FunctionRequirement] 
    params: DeploymentParams
    # Elements populated after deployment 
    code_location: Path
    uid : str = ''
    handler: str = 'handler' # Code compilation defaults to generating a function handler 
    is_deployed: bool = False

class FunctionCompiler(BaseCompiler):
    """
    Compiles business logic
     
    Can add elements to the graph.
    Can iterate over the parse tree and compile the code.
    Tree structure allows the nodes to take their context
    into account when creating code fragments.
    """
    def __init__(self, 
        compiler: BaseCompiler, #Actually the parent Compiler. Used to access the other compiler to request resource allocation dynamically
        compilation_dir: str='./ingestless/restmap/src', 
        language:str="Python@3.9",

        ) -> None:
        super().__init__(compilation_dir)

    def compile(self, head: CompilerNode, function: ResolutionGraph) -> FunctionDeployment:
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
        # TODO Make a switch based on the chosen runtime
        code_location = self._save_to_file(doc=code, name=function.name)

        requirements = self._compile_requirements(head)
        deployment_params = self._compile_params()

        return FunctionDeployment(
            code=code,
            handler="handler",
            runtime="PYTHON_3_9",
            requirements= requirements,
            params = deployment_params,
            uid=function.name,
            code_location=code_location
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
        # Extract parameters from graph
        agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9)"
        response_types_allowed = ','.join(['text/html', 'application/xhtml+xml'])
        response_language_allowed = 'en-US'
        cache_max_age = "cache-max-age=0"

        # add nested elements as required
        param_dict = {
            'header': {
                'User-Agent': agent,
                'Accept': response_types_allowed,
                'Accept-Language': response_language_allowed,
                'Cache-Control': cache_max_age
            }
        }
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
        **kwargs
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
            _children=[],
            **kwargs
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
        template: str="functions/aws/request_handler.jinja",
        ) -> HandlerNode.HandlerNode:
        """
        Create the compiled handler Node
        """
        handler = HandlerNode.HandlerNode(
                _template=template, 
                _env=self.env, 
                _parent=None, 
                _children=[], 
                _code='Handler Code\n')
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
        path = self.output_location / f"lambda/{name}"  
        if not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
        path = path / "handler.py" 
        path.write_text(doc) 
        return path


    def _append_to_parent(self, parent: CompilerNode, node: CompilerNode):
        """Appends to given parent, or else to Compilation Tree root"""
        parent.child(node) 


