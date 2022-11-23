
import pytest
from pathlib import Path
from restmap.manager.Manager import Manager
from restmap.resolver.ResolutionGraph import ResolutionGraph
from restmap.compiler.Compiler import Compiler
from restmap.compiler.function.FunctionCompiler import FunctionCompiler, DeployableFunction, DeploymentParams 
from restmap.compiler.function import HeaderNode, HandlerNode

@pytest.fixture
def compiler():
    return Compiler()

@pytest.fixture
def func_compiler():
    return FunctionCompiler()

@pytest.fixture()
def template_path():
    return Path('./ingestless/tests/restmap/assets/complex_endpoint.yml')

@pytest.fixture
def graph(template_path, manager: Manager):
    return manager._parser.load(template_path)

@pytest.fixture
def manager():
    return Manager(backend='AWS', name="TestStack")

class TestCompiler:
    """
    Tests the compiler class implementing the compilation API
    towards the Manager Class. All construct specific compilers
    are managed through this Compiler class.
    """

    def test_from_resolution_graph_endpoint(self, manager: Manager, compiler: Compiler):
        template = manager._parser.load('./ingestless/tests/restmap/assets/complex_endpoint.yml')
        resolution_graph = manager._resolver.resolve(template)
        deployables = compiler.from_resolution_graph(resolution_graph)
        assert all([isinstance(d, DeployableFunction) for d in deployables])
        # TODO Generalize to all types of supported entities
        for deployment in deployables:
            assert isinstance(deployment, DeployableFunction), "Compiling a function must return a DeployableFunction instance"
            assert isinstance(deployment.code, str), "Compiled code must be returned as a string"
            assert isinstance(deployment.params, DeploymentParams), "Deployment Parameters must be compiled to a DeploymentParams instance"
        # Assert a python file is generated in the target src location

    #TODO Extend list of parsable constructs, to enable parsing of folder structures like Kubernetes
    def test_from_resolution_graph_resolver(self, manager: Manager, compiler: Compiler):
        raise NotImplementedError

class TestFunctionCompiler:

    def test_initialize_graph(self, func_compiler: FunctionCompiler):
        assert isinstance(func_compiler, FunctionCompiler)

    def test_add_header(self, compiler: Compiler, func_compiler: FunctionCompiler):
        head = compiler._spawn_head()
        header_node = func_compiler.header(head)
        assert isinstance(header_node, HeaderNode.HeaderNode)
        assert len(compiler.heads) == 1, "calling head without parent defined must create parallel compilation tree"
        

    def test_add_request_handler(self, compiler: Compiler, func_compiler: FunctionCompiler):
        head = compiler._spawn_head()
        handler_node = func_compiler.request(head)
        assert isinstance(handler_node, HandlerNode.HandlerNode)
        assert len(compiler.heads) == 1, "calling head without parent defined must create parallel compilation tree"
        assert compiler.heads[0]._children[0] == handler_node
    
    def test_add_nested_request_handler(self, compiler: Compiler, func_compiler: FunctionCompiler):
        head = compiler._spawn_head()
        handler = func_compiler.request(
            template='functions/api_request.jinja',
            parent=head
        )
        auth = func_compiler.authenticator(handler)
        handler.compile_code()
        assert isinstance(handler, HandlerNode.HandlerNode)
        assert len(compiler.heads) == 1, "calling head without parent defined must create parallel compilation tree"
        assert compiler.heads[0]._children[0] == handler
        assert len(handler._children) == 1
        assert handler._children[0] == auth
        # Introduce nested elements

    def test_compile_header(self, compiler: Compiler, func_compiler: FunctionCompiler):
        head = compiler._spawn_head()
        handler = func_compiler.request(
            parent=head,    
            template='functions/api_request.jinja'
        )
        response = handler.compile_code()
        assert response
        assert isinstance(response, str)
        
    def test_compile_body_parser(self, compiler: Compiler, func_compiler: FunctionCompiler):
        head = compiler._spawn_head()
        parser = func_compiler.body_parser(head)
        response = parser.compile_code()
        assert response
        assert isinstance(response, str)

    def test_compile(self, graph: ResolutionGraph, compiler: Compiler, func_compiler: FunctionCompiler):
        # Compiler manages the heads, ResolutionGraph defines the attributes for compilation of constructs 
        function = graph._endpoints[0] 
        head = compiler._spawn_head()
        function_deply = func_compiler.compile(function, head)
        # Assert there is a response object that is a string
        assert isinstance(function_deply, DeployableFunction), "Compiling a function must return a DeployableFunction instance"
        assert isinstance(function_deply.code, str), "Compiled code must be returned as a string"
        assert isinstance(function_deply.params, DeploymentParams), "Deployment Parameters must be compiled to a DeploymentParams instance"
        # Assert a python file is generated in the target src location
        # Assert 
    

class TestCompilerNode:

    def test_compile_flat_construct(self, manager: Manager, func_compiler: FunctionCompiler):
        head = manager._compiler._spawn_head()
        header = func_compiler.header(head)
        assert header

    def test_compile_subtree(self, manager: Manager, func_compiler: FunctionCompiler):
        head = manager._compiler._spawn_head()
        header = func_compiler.header(head)
        auth = func_compiler.authenticator(header)
        output = header.compile()
        assert isinstance(output, str)    
    
    def test_render_template(self, manager: Manager, func_compiler: FunctionCompiler):
        head = manager._compiler._spawn_head()
        header = func_compiler.header(head)
        response = header.compile_code()
        assert isinstance(response, str), "Must return a code string rendered by the template"
        #TODO Extend the assertions on the template rendering process applied here