# Caching

## Domain

Systems Engineering

## Topic

Caching

## Overview

Caching stores frequently accessed data closer to the application
so that future requests can be served faster.

Caches can reduce latency and reduce load on databases or other
backend services.

## Common Use Cases

- Frequently accessed database records
- API responses
- Session data
- Computed results
- Frequently requested configuration

## Key Considerations

### Cache Hit Rate

A high cache hit rate can reduce the number of requests sent to
the underlying data source.

### Latency

Memory-based caches can provide significantly lower latency than
retrieving data from slower storage systems.

### Expiration

Cached data can use expiration policies such as TTL to prevent
stale entries from remaining indefinitely.

### Consistency

Caching introduces a risk that cached data may become stale.

Applications need an appropriate invalidation or refresh strategy.

### Memory

Caches typically have limited memory capacity, so eviction
policies may be required.

### Failure Handling

Applications should consider what happens when the cache becomes
unavailable or loses its data.

## Trade-offs

Caching can improve application performance and reduce backend
load.

However, it introduces additional system complexity and requires
careful handling of stale data, invalidation, memory limits,
and cache failures.

## Source

Engineering Knowledge Base