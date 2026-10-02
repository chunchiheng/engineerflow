# Amazon EC2

## Domain

Cloud Engineering

## Topic

Virtual Machines

## Overview

Amazon EC2 provides resizable virtual servers in the AWS cloud.
Engineers can choose instance types, operating systems, storage,
networking configurations, and scaling strategies based on
application requirements.

## Common Use Cases

- Web applications
- Long-running services
- Custom runtime environments
- Applications requiring operating system control
- Compute-intensive workloads
- Applications with specialized software requirements

## Key Considerations

### Infrastructure Management

EC2 provides significant control over the operating system and
runtime environment, but engineers are responsible for more
infrastructure management compared with serverless services.

### Instance Sizing

Engineers need to select appropriate instance types and sizes
based on CPU, memory, network, and workload requirements.

### Scaling

Applications may use Auto Scaling to add or remove instances
based on workload demand.

### Availability

Production applications should consider multiple Availability
Zones and appropriate load balancing strategies.

### Cost

EC2 typically uses instance-based pricing. Running instances
continuously can result in ongoing infrastructure costs.

### Security

Engineers need to manage operating system updates, security
configuration, IAM permissions, network controls, and access
policies.

### Networking

EC2 integrates with VPC networking and provides control over
subnets, security groups, routing, and network interfaces.

### Observability

Production EC2 workloads should consider monitoring,
logging, metrics, alerting, and system-level diagnostics.

## Trade-offs

EC2 provides greater control and flexibility over the computing
environment, but this comes with additional infrastructure
management responsibilities.

It is often suitable when applications require long-running
processes, custom environments, or greater control over the
underlying operating system.

## Source

AWS Documentation

## URL

https://docs.aws.amazon.com/ec2/