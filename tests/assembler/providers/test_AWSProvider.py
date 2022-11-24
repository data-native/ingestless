import pytest
from manager.provider.AWS.AWSProvider import AWSProvider, BackendProvider
from restmap.executor.AWS.bucket import BucketProvider
from restmap.executor.AWS.function import FunctionProvider
from restmap.compiler.function.FunctionCompiler import FunctionDeployment, FunctionRequirement, FunctionDeploymentConfig

@pytest.fixture
def provider():
    """Instantiates the BackendProvider along all registered ConstructProviders"""
    return BackendProvider('MyStack')

class TestSetup:

    def test_init_stack(self, provider: BackendProvider):
        assert provider
        assert False

class TestBucketProvider:

    def test_create_bucket(self, provider: BackendProvider):
        bucket_name = 'test'
        bucket = provider.Bucket.bucket(bucket_name)
        bucket.withRole('test')
        assert bucket_name in provider._bucketProvider._constructs
         
    def test_synth_bucket(self, provider: BackendProvider):
        bucket_name = 'test'
        bucket = provider.Bucket.bucket(bucket_name)
        provider.compile()

class TestFunctionProvier:

    def test_get_provider(self, provider: BackendProvider):
        func_provider = provider.Function
        assert isinstance(func_provider, FunctionProvider)
    def test_create_function(self, provider: BackendProvider):
        function_config = FunctionDeployment(
            code='Some Code', 
            requirements=[FunctionRequirement()],
            params= FunctionDeploymentConfig()
        )
        function = provider.Function.function(function_config)
    