"""
Catalog Agent
-------------
AI agent responsible for intelligent product discovery,
semantic search, recommendations, and catalog explanations
using RAG + LLM orchestration.

Domain: eCommerce (B2C / B2B)
"""

from typing import Dict, List, Any
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage
from langchain.tools import tool

# -----------------------------
# LLM Configuration
# -----------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)

# -----------------------------
# Tools (Microservice + RAG)
# -----------------------------

@tool
def semantic_catalog_search(query: str) -> List[Dict[str, Any]]:
    """
    Semantic search over product catalog using vector DB.
    """
    # Real impl → embedding + FAISS/Chroma search
    return [
        {
            "sku": "SKU123",
            "name": "Noise Cancelling Headphones",
            "price": 2999,
            "category": "Electronics",
            "features": ["ANC", "Bluetooth", "40h Battery"]
        },
        {
            "sku": "SKU456",
            "name": "Wireless Earbuds Pro",
            "price": 1999,
            "category": "Electronics",
            "features": ["Noise Reduction", "Fast Charging"]
        }
    ]


@tool
def get_product_details(sku: str) -> Dict[str, Any]:
    """
    Fetch detailed product data from Catalog Service (Java).
    """
    return {
        "sku": sku,
        "description": "High-quality audio device with premium features.",
        "availability": "IN_STOCK",
        "rating": 4.5,
        "b2b_pricing_available": True
    }


@tool
def get_inventory_status(sku: str) -> str:
    """
    Inventory check from Inventory microservice.
    """
    return "Available for immediate dispatch"


@tool
def get_b2b_pricing(customer_id: str, sku: str) -> Dict[str, Any]:
    """
    Fetch contract-based B2B pricing.
    """
    return {
        "contract_price": 2499,
        "min_order_qty": 10,
        "discount_percent": 15
    }


# -----------------------------
# Prompt Template
# -----------------------------
catalog_prompt = PromptTemplate(
    input_variables=[
        "query",
        "products",
        "customer_type",
        "pricing_info"
    ],
    template="""
You are an AI Catalog Agent for an enterprise eCommerce platform.

Customer Type: {customer_type}
Search Query: "{query}"

Matching Products:
{products}

Pricing Information:
{pricing_info}

Your task:
1. Explain product differences clearly
2. Recommend the best option based on intent
3. Mention availability and pricing context
4. Keep the tone concise and professional
"""
)

# -----------------------------
# Agent Orchestration Logic
# -----------------------------
def handle_catalog_query(
    query: str,
    customer_type: str = "B2C",
    customer_id: str | None = None
) -> Dict[str, Any]:
    """
    Orchestrates catalog discovery and recommendation workflow.
    """

    # Step 1: Semantic search (RAG)
    products = semantic_catalog_search.run(query)

    enriched_products = []
    pricing_info = {}

    # Step 2: Enrich product details
    for product in products:
        details = get_product_details.run(product["sku"])
        inventory = get_inventory_status.run(product["sku"])

        product.update(details)
        product["inventory"] = inventory
        enriched_products.append(product)

        # Step 3: B2B pricing logic
        if customer_type == "B2B" and customer_id:
            pricing_info[product["sku"]] = get_b2b_pricing.run(
                customer_id, product["sku"]
            )

    # Step 4: Generate AI response
    prompt = catalog_prompt.format(
        query=query,
        products=enriched_products,
        customer_type=customer_type,
        pricing_info=pricing_info or "Standard pricing applies"
    )

    ai_response: AIMessage = llm.invoke(prompt)

    return {
        "products": enriched_products,
        "message": ai_response.content
    }


# -----------------------------
# Example Invocation
# -----------------------------
if __name__ == "__main__":
    response = handle_catalog_query(
        query="best noise cancelling headphones",
        customer_type="B2C"
    )

    print(response)

