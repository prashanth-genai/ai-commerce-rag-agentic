# ai-commerce-rag-agentic
AI-powered B2C/B2B eCommerce assistant integrated with existing Java microservices (HCL Commerce style)
# ⭐ AI-Commerce RAG + Agentic Platform  
### Intelligent Commerce Engine powered by GenAI, RAG, and LangGraph

This repository implements a **production-ready AI layer** on top of existing **Java-based eCommerce microservices** (Catalog, Order/OMS, Pricing, Inventory, Shipping).  
It uses:

- **LLMs (GPT-4o family)**
- **LangGraph multi-agent orchestration**
- **RAG (FAISS / Chroma vector DB)**
- **FastAPI AI Gateway**
- **Java microservice integration**

The goal is to bring **AI automation** to B2C/B2B commerce platforms such as **HCL Commerce, SAP Commerce, and Spring Boot microservices**.

---

## 🚀 Key Features

### ✔ Multi-Agent Architecture (LangGraph)
- Catalog Agent  
- Order Tracking Agent  
- Return Agent  
- Cancellation Agent  
- Pricing Agent (B2B Contracts)

### ✔ RAG (Retrieval-Augmented Generation)
- Catalog embeddings  
- Policy documents  
- Return/cancellation rules  
- Contract pricing documents  

### ✔ FastAPI Gateway
- Authentication (JWT / API Keys)  
- REST endpoints for AI services  
- B2C/B2B integration ready  

### ✔ Java Microservice Integration
- OMS (Order status, cancellations)  
- Catalog service  
- Pricing & contract service  
- Inventory service  
- Shipping ETA service  

### ✔ Fully Tested
- Agent tests  
- API tests  
- Multi-agent workflow tests  
- RAG tests  
- Java-integration mock tests  
- End-to-end tests  
- Load tests (Locust)  
- Chaos tests (resilience)

---

## 🧠 Architecture Overview


