"""
Implements the ProviderInterface
for AWS infrastructure automation

Implements using the AWS CDK
"""

import aws_cdk as cdk
from aws_cdk import App
from .bucket import BucketProvider
class Stack(cdk.Stack):
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
class AWSBackendProvider():

    def __init__(self, name:str) -> None:
        self._scope = App()
        self._stack = self._init_stack(self._scope, construct_id=name)
        self._bucketProvider = BucketProvider(stack=self._stack)
    
    def _init_stack(self,scope:App, construct_id='') -> cdk.Stack:
        return Stack(scope=scope, construct_id=construct_id)
    
    def _init_provider(self):
        """Initialize the management locally for deployment"""
        import subprocess
        status = subprocess.run(["./restmap/assembler/provider/AWS/scripts/init_cdk.sh", ], shell=True) 
        raise NotImplementedError          

    @property
    def Bucket(self) -> BucketProvider:
        """
        Provider for the storage interaface
        """
        return self._bucketProvider

    def deploy(self):
        """Compile and deploy the stack onto the AWS backend"""
        # 
        self.compile()
        raise NotImplementedError

    def compile(self):
        """Compile the iac template for deployment"""
        import subprocess
        status = subprocess.run(["./restmap/assembler/provider/AWS/scripts/init_cdk.sh"], shell=True) 
    
    def diff(self, update):
        """
        Compute the difference between the current deployed stack
        and the updates meant for deployment.
        """
        import subprocess
        return subprocess.run(["cdk", "diff"], shell=True)
    
    def tear_down(self):
        """
        Destroys the stack
        """
        import subprocess
        return subprocess.run(["cdk", "destroy"], shell=True)