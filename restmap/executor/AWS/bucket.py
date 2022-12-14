"""
Implements the bucket interface for the BackendProvider 

Bucket
----------
AWS S3 implementation
"""
import aws_cdk as cdk
import aws_cdk.aws_s3 as s3
from .BaseConstructProvider import BaseConstructProvider

class BucketProvider(BaseConstructProvider):
    """
    Provides a builder interface for bucket instances
    
    Builds resources onto a given stack

    """
    #TODO: Complete implementation of method API

    def __init__(self, stack: cdk.Stack) -> None:
        super().__init__(stack)

    def bucket(self, name: str='') -> 'BucketProvider':
        """
        Create a new S3 bucket
        """
        if name == '':
            return self
        if name in self._constructs:
            return self
        bucket = s3.Bucket(self._stack, id=name)
        self._register_construct(name, bucket)
        self._active_construct = bucket
        return self
    
    def useBucket(self, uid: str) -> 'BucketProvider':
        """Uses an existing bucket for further configuration"""
        # Assumes bucket is in same account
        if uid in self._constructs:
            self._active_construct = self._constructs[uid] 
        else:
            bucket = s3.Bucket.from_bucket_name(self._stack,id=uid, bucket_name=uid)
            self._set_active_construct(bucket)

        return self
    
    def withRole(self, role:str) -> 'BucketProvider':
        """"""
        print(f"Setting role {role} on bucket {self._active_construct}")
        return self
    
    def publicAccess(self, is_public:bool=False):
        """Configure access policies"""
        print(f"Setting access to:  {'public' if is_public else 'private'} on bucket {self._selected_construct}")
        return self
    
    def versioned(self, is_versioned:bool=True):
        """Set versioning on the bucket"""
        return self
