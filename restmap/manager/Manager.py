"""
RestMap Manager

The class provides the management API enabling the initializion
of a local project state, the validation of templates, the registration
of components based on the templates and the management and display of 
the application state.

Overall target is to achieve a highly flexible definition and workflow
management for complex REST API integration processes.

This class relays all functionality to provider classes that house
the business and technical logic.

Overall, the implementation in the RestMap service is independent of 
actual deployment details on a specific backend provider, by compiling all 
activities into the overall serverless abstraction syntax used across the
ingestless framework.
"""


