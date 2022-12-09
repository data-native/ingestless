from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode
from restmap.resolver.nodes.BaseNode import BaseNode 
from ingestless.enums import Services


@dataclass
class LoaderNodeBase:
   pass 
    
    
@dataclass
class LoaderNodeDefaults:
    target:str = ''
    kind:str = ''

@dataclass
class LoaderNode(LoaderNodeDefaults, CompilerNode, LoaderNodeBase):
    """
    The loader specifies the target and method of a data sink offload
    to supported storage targets. 

    This enables not only persistent offloads for storage, but also the 
    pass along of received data from a function through a temporary, decoupled
    storage mechanism such as a queue, pipeline or topic.

    This class manages the dispatch of the storage to the supported targets.
    """
    # TODO The resolved service ARN for the target must be available for compiling the function code 

    def compile_code(self, 
        node: BaseNode,
        child_template:bool=False, 
        parent_template:str='', 
        child_block:str=''
    ) -> str:
        """
        """
        pass
    
    # TODO Define the output methods that can be used within the compiled function components to create the required parametrization/outputs
    def to_queue(self, queue) -> 'LoaderNode':
        """Output the data to a storage queue"""
        self.target = queue
        self.kind = Services.QUEUE
        return self

    def to_bucket(self, bucket: str) -> 'LoaderNode':
        """Output the data to a bucket storage location"""
        self.target = bucket
        self.kind = Services.BUCKET 
        return self         
    
    def to_table(self, table:str) -> 'LoaderNode':
        """Output the data to a table storage"""
        self.target = table
        self.kind = Services.TABLE 
        return self         

    def to_topic(self, topic:str) -> 'LoaderNode':
        """Output data to a topic""" 
        self.target = topic
        self.kind = Services.TOPIC 
        # TODO Impplement compilation process
        return self         