# EngineerFlow

**Multi-Agent AI Engineering Copilot for Technical Research, Architecture Analysis, and Engineering Decision Support**

EngineerFlow is an AI engineering copilot that helps engineers research, analyze, and evaluate complex technical decisions across:

* Cloud Engineering
* AI Engineering
* Systems Engineering

Instead of relying on a single AI agent, EngineerFlow uses specialized engineering agents, a shared engineering knowledge base, previous engineering decisions, and human approval for potentially impactful actions.

---

## Architecture

```text
                         EngineerFlow
                              │
             ┌────────────────┼────────────────┐
             ↓                ↓                ↓
          Cloud              AI             Systems
          Agent             Agent             Agent
             │                │                │
             └────────────────┼────────────────┘
                              ↓
                         Aggregator
                              ↓
                       Action Detector
                              ↓
                    ┌─────────┴─────────┐
                    │                   │
                 Analysis             Action
                    │                   │
                   END            Human Approval
                                        │
                               ┌────────┴────────┐
                               ↓                 ↓
                            Approve            Reject
                               ↓                 ↓
                       Action Executor          END
```

### Supporting Components

```text
                 EngineerFlow
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
      ChromaDB               PostgreSQL
          │                       │
  Engineering Knowledge    Runs & Decisions
                                  │
                              Memory
```

* **ChromaDB** — stores and retrieves engineering knowledge for semantic RAG.
* **PostgreSQL** — stores engineering runs, analysis results, approval state, and previous decisions.
* **Memory** — retrieves relevant historical engineering decisions when useful.
* **Human-in-the-Loop** — requires approval before potentially impactful engineering actions are executed.

---

## Core Capabilities

### Multi-Agent Engineering Analysis

EngineerFlow routes engineering questions to specialized agents:

* **Cloud Agent** — AWS architecture, services, migration, scalability, cost, and security.
* **AI Agent** — LLMs, RAG, embeddings, vector databases, model selection, and AI architecture.
* **Systems Agent** — distributed systems, databases, caching, messaging, performance, and reliability.

The specialized analyses are then combined by an **Aggregator Agent** into a final engineering recommendation.

### Semantic RAG

EngineerFlow maintains an engineering knowledge base covering:

* AWS EC2
* AWS Lambda
* AWS S3
* RAG
* Fine-tuning
* Vector databases
* Kafka
* PostgreSQL
* Caching

Documents are chunked, embedded, stored in ChromaDB, and retrieved based on semantic similarity.

### Engineering Decision Memory

EngineerFlow can search previous engineering runs to find relevant historical decisions.

Previous decisions are treated as **context rather than authoritative answers**, allowing the system to reuse useful engineering experience without blindly following previous recommendations.

### Human-in-the-Loop

Potentially impactful actions such as:

* Deploying infrastructure
* Creating cloud resources
* Deleting resources
* Modifying production infrastructure

require human approval before execution.

The current action executor uses **simulated actions** rather than performing real destructive cloud operations.

---

## Example

EngineerFlow can handle a question such as:

> **Should I migrate my production RAG application from EC2 to Lambda?**

The system can:

1. Identify the relevant engineering domains.
2. Route the problem to Cloud, AI, and Systems agents.
3. Retrieve relevant engineering knowledge using RAG.
4. Consider previous engineering decisions when relevant.
5. Aggregate the specialized analyses.
6. Provide an engineering recommendation.
7. Detect whether the user is requesting an external action.
8. Require human approval before executing an impactful action.

---

## Tech Stack

| Area                | Technology                           |
| ------------------- | ------------------------------------ |
| Language            | Python                               |
| Agent Orchestration | LangGraph                            |
| LLM                 | OpenAI                               |
| RAG                 | LangChain + ChromaDB                 |
| Embeddings          | Hugging Face / Sentence Transformers |
| Database            | PostgreSQL                           |
| Database Platform   | Supabase                             |
| Human-in-the-Loop   | LangGraph `interrupt()`              |
| Version Control     | Git / GitHub                         |

---

## Project Progress

* [x] **M0 — Project Setup**
* [x] **M1 — Product Specification**
* [x] **M2 — Single Engineering Agent**
* [x] **M3 — Tool Calling**
* [x] **M4 — Semantic RAG**
* [x] **M5 — Multi-Agent Orchestration**
* [x] **M6 — PostgreSQL Persistence**
* [x] **M7 — Engineering Decision Memory**
* [x] **M8 — Human-in-the-Loop Approval**
* [ ] **M9 — Async Agent Execution**
* [ ] **M10 — React Dashboard**
* [ ] **M11 — Evaluation**
* [ ] **M12 — Guardrails**
* [ ] **M13 — Docker**
* [ ] **M14 — CI/CD**
* [ ] **M15 — AWS Deployment**
* [ ] **M16 — Final Demo**

---

## Current Status

**M0–M8 completed.**

EngineerFlow currently supports:

```text
Structured Engineering Analysis
            +
Tool Calling
            +
Semantic RAG
            +
Multi-Agent Orchestration
            +
PostgreSQL Persistence
            +
Engineering Decision Memory
            +
Human-in-the-Loop Approval
```

The next milestone is **M9 — Async Agent Execution**, which will introduce background execution so longer engineering workflows do not need to run synchronously from the client.

---

## Project Goal

EngineerFlow is being developed as a practical AI engineering system rather than a simple chatbot.

The project focuses on demonstrating how modern AI applications can combine:

* LLM reasoning
* Agent orchestration
* Tool use
* RAG
* Persistent state
* Engineering memory
* Human oversight
* Asynchronous execution
* Evaluation and guardrails

to support real-world engineering decision-making.
