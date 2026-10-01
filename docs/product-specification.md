# Architecture Specification

| Component | Decision |
| :--- | :--- |
| **Product** | Engineering Decision Copilot |
| **Domains** | Cloud + AI + Systems |
| **Cloud focus** | AWS first |
| **Orchestrator** | Supervisor |
| **Specialized Agents** | Cloud / AI / Systems |
| **Simple query** | Single agent |
| **Complex query** | Multi-agent |
| **RAG** | Curated Engineering KB |
| **Web** | Live search |
| **Tools** | Calculation / external operations |
| **Database** | PostgreSQL |
| **Vector DB** | ChromaDB |
| **Workflow** | LangGraph |
| **HITL (Human-in-the-Loop)**| External actions |
| **Backend** | FastAPI |
| **Frontend** | React |
| **Async** | Redis + Celery |
| **Deployment** | Docker → AWS |
| **Evaluation** | Retrieval + Agent + LLM + System |
| **Security** | Guardrails + prompt injection + audit logs |