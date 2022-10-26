# IngestLess - Serverless Data Ingestion orchestration framework

The framework develops a low cost, self-maintained alternative to the premium AWS orchestration services.

## Functionality
Feature | Component  | Available with version
------ | -------- | ----------
Set a cron trigger on an ingestion function | Orchestrator | 1.0
Register a lambda function for orchestration  | Manager | 1.0
Keep state of the execution for all pipelines | Orchestrator | 1.0
 Register an event for orchestration | Manager | 1.0


 ## Orchestration
 The service allows users to trigger lambdas in an event driven, or a trigger based fashion

 ### Trigger based orchestration
Schedule the execution of an lambda based on timed intervals in cron jobs. 
 ### Event based orchestration
Register a set of events that can be triggered from within a lambda function asynchronously to orchestrate itself with other lambdas 

## Dependency resolution 
Enables lambda functions dependencies to resolve when new data has become available at the successfull comp;letion of previous executions. 

* Central metadata table stores distributed state of all registered function dependencies
* Registration of dependencies happens against the table names registered in the metadata catalog shared across the platform
* 
