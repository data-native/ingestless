import pytest
from restmap.compiler.Compiler import PythonCompiler, HeaderNode, HandlerNode

@pytest.fixture
def compiler():
    return PythonCompiler()

class TestFunctionCompilation:

    def test_initialize_graph(self, compiler: PythonCompiler):
        assert isinstance(compiler, PythonCompiler)

    def test_compile_header(self, compiler: PythonCompiler):
        header_node = compiler.header()
        assert isinstance(header_node, HeaderNode)
        assert compiler.head.children[0] == header_node

    def test_compile_http_request(self, compiler: PythonCompiler):
        handler_node = compiler.handler()
        assert isinstance(handler_node, HandlerNode)
        assert compiler.head.children[0] == handler_node

    def test_compile_body_parser(self, compiler: PythonCompiler):
        assert False

    def test_compile_response_covertion(self, compiler: PythonCompiler):
        assert False

    def test_compile_response_offload(self, compiler: PythonCompiler):
        assert False

    def test_compile(self, compiler: PythonCompiler):
        compiler.header()
        compiler.handler()
        compiler.compile()
        assert compiler.code != ''
