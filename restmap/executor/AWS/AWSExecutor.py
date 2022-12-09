"""
Implements the ProviderInterface
for AWS infrastructure automation

Implements using the AWS CDK
"""

import boto3
from typing import Any
import aws_cdk as cdk
from aws_cdk import App
from .provider.bucket import BucketProvider
from .provider.function import FunctionProvider
from .provider.table import TableProvider
from .provider.topic import TopicProvider
from .provider.queue import QueueProvider
from restmap.orchestrator.BaseOrchestrator import OrchestrationGraph

# CONSTRUCT SPECIFIC COMPILERS__________
from restmap.compiler.Compiler import Compiler
from restmap.compiler.function.FunctionCompiler import FunctionCompiler
class Stack(cdk.Stack):
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
class AWSExecutor:
    """
    Implements the configuration and deployment logic
    against AWS using the AWS CDK. 

    Core concepts:

    Stack
    ---------
    """

    def __init__(self, 
        name:str,
        compiler: Compiler
        ) -> None:
        self._compiler = compiler
        # IaC (CDK assets)
        self._scope = App()
        self._stack = self._init_stack(self._scope, construct_id=name)
        self._iac_template = None
        self.clf_client = boto3.client('cloudformation')
        # Provider
        self._bucketProvider = BucketProvider(executor=self, stack=self._stack)
        self._functionProvider = FunctionProvider(executor=self, stack=self._stack)
        self._topicProvider = TopicProvider(executor=self,stack=self._stack)
        self._queueProvider = QueueProvider(executor=self, stack=self._stack)
        #TODO Add additional constructor providers

    def compile_orchestration_graph(self, graph:OrchestrationGraph):
        """
         
        """
        self._compiler.from_orchestration_graph(graph)

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

    @property
    def Table(self) -> TableProvider:
        """
        Provider for the serverless function interface
        """
        return self._functionProvider

    @property
    def Topic(self) -> TopicProvider:
        """
        Provider for the serverless pub/sub topic interface
        """
        return self._topicProvider

    @property
    def Queue(self) -> QueueProvider:
        """
        Provider for the serverless pub/sub topic interface
        """
        return self._queueProvider

    # METHOD API _________________
    # These methods manage the IaC configuration and deployment process
    def compile(self):
        """Compile the iac template based on an orchestrated deployment graph"""
        from aws_cdk.assertions import Template
        # Just compiles the configured stack, does not own any logic.
        # Business logic is placed in the orchestrator
        self._scope.synth()
        template = Template.from_stack(self._stack)
        self._iac_template = template
        # Save the file to the correct location

    def deploy(self):
        """Compile and deploy the stack onto the AWS backend"""
        import boto3
        import json
        if not self._iac_template:
            self.compile()
        response = self.clf_client.create_stack(
            StackName='test', 
            TemplateBody=json.dumps(self._iac_template.to_json()), 
            Parameters=[], 
            DisableRollback=False, 
            TimeoutInMinutes=2, 
            Tags=[]
        )
        return response
         
    def diff(self, update):
        """
        Compute the difference between the current deployed stack
        and the updates meant for deployment.
        """
        self.compile()
        self.clf_client 
        # Get the 
    
    def tear_down(self, stack:str):
        """
        Destroys the stack
        """
        try:
            response = self.clf_client.delete_stack(StackName=stack)
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise ConnectionError("The connection was refused. Please try again")
        except Exception as e:
            raise(e)
