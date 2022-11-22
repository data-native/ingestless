import aws_cdk as cdk

class BaseConstructProvider:
    """
    Implements general methods used to manager
    all constructs within the AWS CDK framework
    """
    def __init__(self, stack: cdk.Stack) -> None:
        self._stack = stack
        self._constructs = {}
        self._selected_construct = None
    
    def _register_construct(self, name: str, construct):
        """Cache a construct locally"""
        if name not in self._constructs:
            self._constructs[name] = construct 

    def _get_active_construct(self):
        return self._selected_construct

    def _set_active_construct(self, construct):
        self._selected_construct = construct