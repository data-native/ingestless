"""
Implements the ProviderInterface
for AWS infrastructure automation

Implements using the AWS CDK
"""

import aws_cdk as cdk
from aws_cdk import App
from .bucket import BucketProvider
from .function import FunctionProvider

class Stack(cdk.Stack):
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
class AWSBackendProvider():
    """
    Implements the configuration and deployment logic
    against AWS using the AWS CDK. 

    Core concepts:

    Stack
    ---------
    """

    def __init__(self, name:str) -> None:
        self._scope = App()
        self._stack = self._init_stack(self._scope, construct_id=name)
        self._bucketProvider = BucketProvider(stack=self._stack)
        self._functionProvider = FunctionProvider(stack=self._stack)
        #TODO Add additional constructor providers
    
    def _init_stack(self,scope:App, construct_id='') -> cdk.Stack:
        return Stack(scope=scope, construct_id=construct_id)
    
    def _init_provider(self):
        """Initialize the management locally for deployment"""
        import subprocess
        status = subprocess.run(["cdk", "compile", ], shell=True) 
        raise NotImplementedError          

    # CONSTRUCTORS ____________________
    # Grant access to the type specific constructors through a unfied class interface
    @property
    def Bucket(self) -> BucketProvider:
        """
        Provider for the storage interaface
        """
        return self._bucketProvider
    
    @property
    def Function(self) -> FunctionProvider:
        """
        Provider for the serverless function interface
        """
        return self._functionProvider


    # METHOD API _________________
    # These methods manage the IaC configuration and deployment process
    def deploy(self):
        """Compile and deploy the stack onto the AWS backend"""
        # 
        self.compile()
        raise NotImplementedError

    def compile(self):
        """Compile the iac template for deployment"""
        raise NotImplementedError
         
    def diff(self, update):
        """
        Compute the difference between the current deployed stack
        and the updates meant for deployment.
        """
        import subprocess
        return subprocess.run(["cdk", "synth"], shell=True)
    
    def tear_down(self):
        """
        Destroys the stack
        """
        import subprocess
        return subprocess.run(["cdk", "destroy"], shell=True)