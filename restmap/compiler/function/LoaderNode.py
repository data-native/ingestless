from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode
from restmap.resolver.nodes.BaseNode import BaseNode 


@dataclass
class LoaderNodeBase:
    target: str 
    
@dataclass
class LoaderNodeDefaults:
    pass

@dataclass
class LoaderNode(LoaderNodeDefaults, CompilerNode, LoaderNodeBase):

    def compile_code(self, 
        node: BaseNode,
        child_template:bool=False, 
        parent_template:str='', 
        child_block:str=''
    ) -> str:
        """
        """
    
    # TODO Define the output methods that can be used within the compiled function components to create the required parametrization/outputs
    def sink_to_bucket(self, bucket: str):
        """Output the data to a bucket storage location"""
        raise NotImplementedError
    
    def sink_to_table(self, table:str):
        """Output the data to a table storage"""
        raise NotImplementedError
    
    def sink_to_queue(self, queue:str):
        """Output the data to a storage queue"""
        raise NotImplementedError
