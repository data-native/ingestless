import aws_cdk as cdk

class BaseConstructProvider:
    """
    Implements general methods used to manager
    all constructs within the AWS CDK framework
    """
    def __init__(self, stack: cdk.Stack) -> None:
        self.stack = stack
        self._constructs = {}
        self._construct_in_scope = None
    

    def get_active_construct(self):
        return self._construct_in_scope.construct

    def use(self, construct: str) -> 'BaseConstructProvider':
        return ConstructContextManager(provider=self, construct=construct)

    def compile(self):
        """
        Compiles the configuration into code after changes are applied.

        Enables already compiled functions to be changed dynamically when
        required as part of the orchestration process. 
        """
        construct = self._construct_in_scope
        # Trigger comilation process again

    def _register_construct(self, name: str, construct):
        """Cache a construct locally"""
        if name not in self._constructs:
            self._constructs[name] = construct 

    def _select_construct(self, construct):
        self._construct_in_scope = construct

    def _ensure_construct_scope(self):
        if not self._construct_in_scope:
            raise ValueError("No active construct scope set. Use `with provider.use(CONSTRUCTNAME) as ..` to manage a specific construct")

class ConstructContextManager:
    """
    
    """
    def __init__(self, provider: BaseConstructProvider, construct: str) -> None:
        self.provider = provider
        self.selected_construct = construct

    def __enter__(self) -> BaseConstructProvider:
        try:
            construct = self.provider._constructs[self.selected_construct]
            self.provider._select_construct(construct)
            return self.provider 
        except KeyError:
            raise KeyError(f"No function {self.selected_construct} registered. If configured, register the function with the Provider first.") 

    def __exit__(self, exception_type, exception_value, traceback):
        self.provider._construct_in_scope = None