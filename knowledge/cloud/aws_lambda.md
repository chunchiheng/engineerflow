# AWS Lambda

## Domain

Cloud Engineering

## Topic

Serverless Compute

## Overview

AWS Lambda is a serverless compute service that allows engineers
to run code without managing servers directly.

Lambda automatically manages the underlying compute infrastructure
and can scale the number of running executions based on incoming
requests or events.

## Common Use Cases

- REST APIs
- Event-driven applications
- Background processing
- Scheduled tasks
- Data processing
- Lightweight microservices

## Key Considerations

### Execution Duration

Lambda functions have execution duration limits, so workloads
that require long-running processes may be better suited to
other compute services.

### Cold Starts

A Lambda function may experience additional latency when a new
execution environment needs to be initialized.

### Concurrency

Lambda can execute multiple function instances concurrently.
Engineers should consider concurrency limits and downstream
service capacity.

### Memory and CPU

Lambda resources are allocated based on the configured memory.
Increasing memory also provides more CPU resources.

### Cost

Lambda uses a usage-based pricing model. Cost depends on factors
such as the number of requests and execution duration.

### Networking

Lambda functions can access resources in a VPC, but networking
configuration can introduce additional complexity and latency.

### State

Lambda functions should generally be designed to be stateless.
Persistent state should be stored in external services such as
databases or object storage.

### Observability

Production Lambda applications should consider logging,
metrics, tracing, error handling, and monitoring.

## Trade-offs

Lambda reduces infrastructure management and works well for
event-driven and variable workloads.

However, engineers need to consider execution limits,
cold starts, concurrency, networking complexity, and
potential platform-specific constraints.

## Source

AWS Documentation

## URL

https://docs.aws.amazon.com/lambda/