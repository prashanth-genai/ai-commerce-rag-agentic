# Multi-Agent Design (LangGraph)

This document describes how multi-agent workflows operate.

---

## 1. Agents Involved

- CatalogAgent
- OrderAgent
- ReturnAgent
- CancelAgent
- PricingAgent (B2B)
- IntentClassifier (LLM)
- RAGRetriever

---

## 2. AgentGraph Flow

┌──────────────────┐
User ---> │ Intent Classifier │
└───────┬──────────┘
↓
┌───────────────────────┐
│ Conditional Router │
└────────┬───────┬──────┘
│ │
┌───────▼──┐ ┌──▼───────────┐
│ Catalog │ │ Order Agent │
└───────────┘ └──────────────┘
│ │
┌───────▼──┐ ┌──▼───────────┐
│ Return │ │ Cancel Agent │
└───────────┘ └──────────────┘
↓
END

yaml
Copy code

---

## 3. Why LangGraph?

- Deterministic execution  
- Orchestrates multiple agents  
- Supports memory + traceability  
- Works well in enterprise production  

---

## 4. Agent Responsibilities

### Catalog Agent
✔ Semantic search  
✔ Product comparison  

### Order Agent
✔ Real-time OMS status  
✔ ETA reasoning  

### Return Agent
✔ Policy-based return eligibility  
✔ Refund computation  

### Cancellation Agent
✔ Shipment-state validation  
✔ Policy-driven eligibility  

### Pricing Agent
✔ Contract pricing  
✔ Tier-based B2B discounts  

---

## 5. State Management

state = {
"user_query": "...",
"intent": "order_status",
"result": {...}
}

---

## 6. Traceability

Each node logs:

- Input  
- Output  
- Tool calls  
- Errors  

---


