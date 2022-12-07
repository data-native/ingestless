from dataclasses import dataclass
from restmap.compiler.CompilerNode import CompilerNode
from restmap.resolver.nodes.BaseNode import BaseNode 
from restmap.resolver.nodes.EndpointNode import RelativeURLNode
from restmap.resolver.nodes.resolvers import ResolverNode

from pathlib import Path

@dataclass
class HeaderNodeBase:
    params: dict
    
@dataclass
class HeaderNodeDefaults:
    UserAgent: str = "TestAgent: Chrome"
    Accept: str = "text/html, application/json"
    AcceptLanguage: str = 'en-US'
    cache_max_age = "cache-max-age=0"

@dataclass
class HeaderNode(HeaderNodeDefaults, CompilerNode, HeaderNodeBase):

    def compile_code(self, 
        node: BaseNode,
        child_template:bool=False, 
        parent_template:str='', 
        child_block:str=''
    ) -> str:
        """
        The header configuration is compiled 
        based on the parametrization of the request template
        
        return: A configuration dict passed 
        @child_template: Ask node to render into child template
        @parent_template(opt): When child_template it identifies the name of the parent template
        @child_block(opt): When child_template it names the block into which to render in the parent
        """
        # TODO Enable the selection of a specific Agent
        # TODO Define a speicif language return
        # TODO Specify authentication header elements

        # Retrieve the list of parameters set on the inh
        # Call the set of functions to generate the code
        template_params = self.params | {
            'content': 'not set' 
        } 
        # Conditionally render the parameter resolutions
        # TODO Resolve the identity of the parameters send out by the resolvers
        rendered = self._render_template(template_params)

        # TODO Fix the indentation on this code nesting
        if child_template:
            # The Node is asked to render itself as a block within a parent
            # Add the {% extends line %}
            extension_str = f"""{{% extends "{parent_template}" %}}\n"""
            # It is then wrapped in the child block statement
            wrapping_start = f"""{{% block {child_block}}}"""
            wrapping_end = f"""{{% endblock %}}"""
            rendered = extension_str + wrapping_start + rendered + wrapping_end
            
        return rendered

    def randomize_agents(self):
        raise NotImplementedError

    def encrypt_traffic(self):
        raise NotImplementedError