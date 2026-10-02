# Amazon S3

## Domain

Cloud Engineering

## Topic

Object Storage

## Overview

Amazon S3 is an object storage service designed to store and
retrieve data at scale.

Data is stored as objects inside buckets. S3 can be used for
application data, backups, static assets, logs, and data
processing workloads.

## Common Use Cases

- Backup and archival
- Static website assets
- Data lakes
- Application file storage
- Log storage
- Machine learning datasets

## Key Considerations

### Storage Model

S3 uses object storage rather than a traditional filesystem.
Applications interact with objects through APIs.

### Durability

S3 is designed for highly durable storage and provides
multiple storage classes for different access patterns.

### Storage Classes

Different storage classes can be selected based on access
frequency, retrieval requirements, and cost considerations.

### Security

Engineers should consider IAM policies, bucket policies,
encryption, access controls, and public access settings.

### Performance

S3 can support high request rates, but application architecture
should still consider request patterns, object sizes, and
network latency.

### Cost

Costs can depend on storage volume, requests, data retrieval,
and data transfer.

### Lifecycle Management

Lifecycle policies can automatically transition or delete objects
based on defined rules.

## Trade-offs

S3 provides scalable object storage with relatively low
infrastructure management overhead.

However, it is not a general-purpose filesystem and applications
need to consider object-based access patterns, data transfer,
retrieval costs, and access controls.

## Source

AWS Documentation

## URL

https://docs.aws.amazon.com/s3/