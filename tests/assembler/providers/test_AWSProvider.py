import pytest
from restmap.assembler.provider.AWS.AWSProvider import AWSBackendProvider, FunctionProvider
from restmap.assembler.provider.AWS.bucket import BucketProvider
from restmap.compiler.function.FunctionCompiler import DeployableFunction, FunctionRequirement, FunctionDeploymentConfig

@pytest.fixture
def provider():
    """Instantiates the BackendProvider along all registered ConstructProviders"""
    return AWSBackendProvider('MyStack')


class TestSetup:

    def test_init_stack(self, provider: AWSBackendProvider):
        assert provider
        assert False

class TestBucketProvider:

    def test_create_bucket(self, provider: AWSBackendProvider):
        bucket_name = 'test'
        bucket = provider.Bucket.bucket(bucket_name)
        bucket.withRole('test')
        assert bucket_name in provider._bucketProvider._constructs
         
    def test_synth_bucket(self, provider: AWSBackendProvider):
        bucket_name = 'test'
        bucket = provider.Bucket.bucket(bucket_name)
        provider.compile()

class TestFunctionProvier:

    def test_get_provider(self, provider: AWSBackendProvider):
        func_provider = provider.Function
        assert isinstance(func_provider, FunctionProvider)
    def test_create_function(self, provider: AWSBackendProvider):
        function_config = DeployableFunction(
            code='Some Code', 
            requirements=[FunctionRequirement()],
            params= FunctionDeploymentConfig()
        )
        function = provider.Function.function(function_config)
    