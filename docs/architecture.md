# AI-Commerce Agentic Platform – Architecture Overview

## 1. System Overview

The AI-Commerce platform adds an **AI Intelligence Layer** on top of an existing
eCommerce system (HCL Commerce / Java Microservices).  
It uses:

- RAG (Retrieval-Augmented Generation)
- Multi-Agent System (LangGraph)
- FastAPI Gateway
- Vector Database (FAISS/Chroma)
- Java microservices (Catalog, Order, Pricing, OMS)

The architecture ensures **zero disruption** to existing commerce flows.

---

## 2. High-Level Architecture Diagram
User (Web/Mobile/CSR)
|
API Gateway (FastAPI + Auth)
|
| Multi-Agent Engine (LangGraph) |
| - Intent Classifier |
| - Catalog Agent |
| - Order Agent |
| - Return Agent |
| - Cancellation Agent |
| - Pricing Agent |
RAG Layer (Vector DB + Embeddings + Policies)
|
Java Commerce Microservices (Existing Platform)
| Catalog | OMS | Pricing | Inventory | Shipping |

---

## 3. AI Layer Components

### **3.1 AgentGraph (LangGraph)**  
Responsible for:

- Intent detection  
- Routing  
- Multi-step workflows  
- Stateful context passing  

### **3.2 Agents**

| Agent | Responsibility |
|-------|---------------|
| Catalog Agent | Semantic search, product explanation |
| Order Agent | Tracking, ETA reasoning |
| Return Agent | Return eligibility + refund logic |
| Cancel Agent | Validate cancellation rules |
| Pricing Agent | B2B pricing, contract pricing |

---

## 4. RAG Layer

- Embeds catalog, FAQs, return policy, shipping rules
- Stores vectors in **FAISS / Chroma**
- Ground LLM responses to **prevent hallucination**

---

## 5. Integration Layer (Java Microservices)

The AI layer communicates with commerce services via REST:

- Catalog APIs  
- OMS APIs  
- Pricing / Contract APIs  
- Inventory APIs  
- Shipping APIs  

This keeps the architecture **polyglot** and production-ready.

---

## 6. Deployment

- Docker containers  
- Optionally deployed via Kubernetes  
- CI/CD with GitHub Actions  
- ConfigMaps for environment variables  



