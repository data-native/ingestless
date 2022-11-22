import pytest
from restmap.manager.Manager import Manager
from restmap.compiler.function.FunctionCompiler import FunctionCompiler
from restmap.compiler.function import HeaderNode, HandlerNode

@pytest.fixture
def func_compiler():
    return FunctionCompiler()

@pytest.fixture
def manager():
    return Manager()

class TestFunctionCompilation:

    def test_initialize_graph(self, func_compiler: FunctionCompiler):
        assert isinstance(func_compiler, FunctionCompiler)

    def test_add_header(self, func_compiler: FunctionCompiler):
        header_node = func_compiler.header()
        assert isinstance(header_node, HeaderNode.HeaderNode)
        assert len(func_compiler.heads) == 1, "calling head without parent defined must create parallel compilation tree"
        assert func_compiler.heads[0]._children[0] == header_node, "Created node must be placed as child of newly created parallel compilation tree"
        

    def test_add_request_handler(self, func_compiler: FunctionCompiler):
        handler_node = func_compiler.request()
        assert isinstance(handler_node, HandlerNode.HandlerNode)
        assert func_compiler.heads[0]._children[0] == handler_node
    
    def test_add_nested_request_handler(self, func_compiler: FunctionCompiler):
        handler = func_compiler.request(
            template='functions/api_request.jinja'
        )
        handler.compile_code()
        # Introduce nested elements

    def test_compile_header(self, func_compiler: FunctionCompiler):
        handler = func_compiler.request(
            template='functions/api_request.jinja'
        )
        handler.compile_code()
        
    def test_compile_body_parser(self, func_compiler: FunctionCompiler):
        parser = func_compiler.body_parser()
        response = parser.compile_code()
        assert response
        assert isinstance(response, str)

    def test_compile(self, func_compiler: FunctionCompiler):
        header = func_compiler.header()
        # handler = func_compiler.handler().retry(20).timeout(10)
        
        response = func_compiler.compile()
        # Assert there is a response object that is a string
        # Assert a python file is generated in the target src location
        # Assert 
        assert response
    
    def test_from_resolution_graph(self, manager: Manager, func_compiler: FunctionCompiler):
        template = manager._parser.load('./ingestless/tests/restmap/assets/complex_endpoint.yml')
        resolution_graph = manager._resolver.resolve(template)
        func_compiler.from_resolution_graph(resolution_graph)
        assert True

class TestCompilerNode:

    def test_compile_flat_construct(self, func_compiler: FunctionCompiler):
        head = func_compiler.header()
        assert head

    def test_compile_subtree(self, func_compiler: FunctionCompiler):
        head = func_compiler.header()
        head.child(func_compiler.authenticator())
        output_head = head.compile_code()
        assert head        