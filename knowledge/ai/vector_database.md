# Vector Databases

## Domain

AI Engineering

## Topic

Vector Database

## Overview

A vector database stores vector representations of data and
supports similarity search.

In AI applications, vector databases are commonly used to
retrieve documents that are semantically similar to a user query.

## Common Use Cases

- Retrieval-Augmented Generation
- Semantic search
- Document retrieval
- Recommendation systems
- Similarity search

## Typical RAG Usage

A RAG system can store document embeddings in a vector database.

When a user submits a query:

1. The query is converted into an embedding.
2. The vector database searches for similar vectors.
3. Relevant documents are retrieved.
4. The documents are provided to the LLM as context.

## Key Considerations

### Similarity Search

The database needs to support efficient similarity search over
high-dimensional vectors.

### Metadata

Documents can be associated with metadata such as domain, source,
title, and topic.

Metadata filtering can restrict retrieval to relevant subsets
of the knowledge base.

### Scale

The appropriate vector storage solution depends on the number
of vectors, query volume, latency requirements, and infrastructure
constraints.

### Retrieval Quality

Vector similarity does not guarantee that retrieved documents
are always relevant. Retrieval strategies and ranking methods
may need to be evaluated.

### Integration

The vector database should integrate effectively with the
application's embedding model and retrieval pipeline.

## Trade-offs

Vector databases simplify semantic retrieval for AI applications,
but system designers still need to consider embedding quality,
metadata filtering, retrieval accuracy, scale, latency, and
operational complexity.

## Source

Engineering Knowledge Base