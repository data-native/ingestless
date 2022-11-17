import pytest
from restmap.assembler.provider.AWS.AWSProvider import AWSBackendProvider
from restmap.assembler.provider.AWS.bucket import BucketProvider

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
         
