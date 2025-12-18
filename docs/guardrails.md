# Guardrails for AI-Commerce Platform

This document describes how we enforce safety and correctness.

---

## 1. Why Guardrails?

- Prevent hallucination  
- Ensure compliance  
- Protect sensitive data  
- Avoid unauthorized workflows  

---

## 2. Types of Guardrails

### 2.1 Input Guard
- Block malicious inputs  
- Foul language detection  
- PII detection  
- SQL/Prompt injection prevention  

### 2.2 Output Guard
- No hallucinated policy statements  
- No fake order IDs  
- No invented prices or refunds  
- Restricted answers (only from context)

---

## 3. RAG-Only Enforcement

System Prompt:


---

## 4. Permission Guardrails

Role-based access:

| Role | Allowed Actions |
|------|------------------|
| CUSTOMER | Browse & track orders |
| CSR | Modify orders, cancel orders |
| AI_AGENT | Full tool access |

---

## 5. Tool-Use Guardrails

LLM cannot:

- Cancel shipped orders  
- Approve refunds without policy  
- Generate return shipment labels  
- Access pricing without authorization  

---

## 6. Logging Everything

All agent steps log:

- Prompt  
- Context  
- Tool calls  
- Final decision  

For audit & compliance.

---


