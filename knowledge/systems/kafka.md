# Apache Kafka

## Domain

Systems Engineering

## Topic

Distributed Messaging

## Overview

Apache Kafka is a distributed event streaming platform designed
to handle high-throughput event streams.

Applications can publish events to Kafka topics and consumers can
process those events independently.

## Common Use Cases

- Event-driven architectures
- Log collection
- Data pipelines
- Streaming analytics
- Microservice communication
- Real-time event processing

## Key Considerations

### Throughput

Kafka is designed to handle high volumes of events across
distributed brokers.

### Partitions

Topics are divided into partitions. Partitions allow data to be
distributed across brokers and enable parallel consumption.

### Consumer Groups

Consumer groups allow multiple consumers to coordinate the
processing of partitions.

### Ordering

Kafka provides ordering guarantees within a partition. Global
ordering across all partitions is not generally provided.

### Durability

Kafka can persist messages to disk and replicate data across
brokers.

### Scaling

Partitions and brokers can be used to distribute workloads.

### Operational Complexity

Running Kafka requires consideration of cluster capacity,
partition management, monitoring, replication, and failure
handling.

## Trade-offs

Kafka is useful for high-throughput event streaming and systems
that require durable event logs.

However, it can introduce more operational complexity than simpler
messaging services.

## Source

Engineering Knowledge Base