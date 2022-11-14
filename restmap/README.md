# RESTLESS
Allows a declarative descripition of rest api ingestion processes. 

## Functionality
Feature | Component | Description
------ | ----- | ----
Can define a REST endpoint through a declarative template | TemplateParser | Provides template schema definitions
Can define resolvers to read attributes from storage location | Resolver | Enables the resolution of targets to read data into iterables for looping constructs
Can define dependency graph amongst data resolution and resolvers | Resolver | Creates an dependency graph based on preliminary requirements amongst the endpoint looping constructs
Can schedule the execution onto a given backend | Scheduler | Generates an abstract schedule based on `serverless semantics` that can be compiled against a `BackendProvider` to create executable instances

# Components
Component | Role
-------- | ---------
Manager | Manage the state of the application and provide overall API
TemplateParser | Parses endpoint templates into `parsegraph` format
Resolver | Resolves dependencies and links in the `parsegraph` input into a `resolved graph`
Scheduler | Optimizes the `resolved graph` into a `schedule` to be send to the backend provider for execution

## Manager

Feature | Subcomponent 
------ | ----------
Register a component based on a template doc | Manager
Unregister a component based on name | Manager
Describe a component based on name | Manager
Initialize state for a given folder location | StateManager
Register expected state based on new component | StateManager
Return expected state | StateManger
Retrieve current state from backend provider | StateManager
Compare current and existing state | StateManager
## TemplateParser
Provides a yaml based, declarative way to create resources. Keeps a backend state to manage deployments and version history to manage roll backs on the ingestion declarations for given endpoints. 

Feature | Subcomponent 
------ | ----------
Check the validity of a template | SchemaParser
Report sections not compliant with the expected schema | SchemaParser
## Resolver 
Resolves

Feature | Subcomponent 
------ | ----------

## Scheduler

