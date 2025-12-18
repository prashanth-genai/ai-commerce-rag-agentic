"""
Return Agent
-------------
Agent responsible for handling return eligibility, refund calculation,
policy validation, and workflow orchestration using RAG + tools.

Domain: eCommerce (B2C / B2B)
"""

from typing import Dict, Any
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage
from langchain.tools import tool

# -----------------------------
# LLM Configuration
# -----------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)

# -----------------------------
# Tools (Microservice Wrappers)
# -----------------------------

@tool
def get_order_details(order_id: str) -> Dict[str, Any]:
    """
    Fetch order details from Order Service (Java Microservice).
    """
    # In real implementation → REST call
    return {
        "order_id": order_id,
        "order_date": "2024-10-01",
        "delivery_date": "2024-10-05",
        "status": "DELIVERED",
        "items": [
            {"sku": "SKU123", "price": 2500, "returnable": True}
        ]
    }


@tool
def get_return_policy(product_sku: str) -> Dict[str, Any]:
    """
    Retrieve return policy using RAG (Vector DB).
    """
    return {
        "return_window_days": 10,
        "restocking_fee_percent": 5,
        "return_type": "REFUND"
    }


@tool
def calculate_refund(price: float, fee_percent: int) -> float:
    """
    Calculate refund amount after restocking fee.
    """
    return round(price - (price * fee_percent / 100), 2)


@tool
def create_return_request(order_id: str, sku: str) -> str:
    """
    Create return request in Order Management System.
    """
    return f"RETURN-{order_id}-{sku}"


# -----------------------------
# Prompt Template
# -----------------------------
return_prompt = PromptTemplate(
    input_variables=[
        "order_id",
        "sku",
        "order_date",
        "delivery_date",
        "price",
        "return_window_days",
        "refund_amount"
    ],
    template="""
You are an AI Return Management Agent for an eCommerce platform.

Order ID: {order_id}
SKU: {sku}
Order Date: {order_date}
Delivery Date: {delivery_date}
Item Price: ₹{price}

Return Policy:
- Return Window: {return_window_days} days
- Refund Amount After Fees: ₹{refund_amount}

Explain clearly:
1. Whether the return is eligible
2. Refund amount
3. Next steps for the customer
Use a professional and customer-friendly tone.
"""
)

# -----------------------------
# Agent Orchestration Logic
# -----------------------------
def handle_return_request(order_id: str, sku: str) -> Dict[str, Any]:
    """
    Main orchestration function for return workflow.
    """

    # Step 1: Fetch order details
    order = get_order_details.run(order_id)
    item = next(i for i in order["items"] if i["sku"] == sku)

    # Step 2: Fetch return policy (RAG)
    policy = get_return_policy.run(sku)

    # Step 3: Calculate refund
    refund_amount = calculate_refund.run(
        price=item["price"],
        fee_percent=policy["restocking_fee_percent"]
    )

    # Step 4: Create return request
    return_id = create_return_request.run(order_id, sku)

    # Step 5: Generate response using LLM
    prompt = return_prompt.format(
        order_id=order_id,
        sku=sku,
        order_date=order["order_date"],
        delivery_date=order["delivery_date"],
        price=item["price"],
        return_window_days=policy["return_window_days"],
        refund_amount=refund_amount
    )

    ai_response: AIMessage = llm.invoke(prompt)

    return {
        "return_id": return_id,
        "refund_amount": refund_amount,
        "message": ai_response.content
    }


# -----------------------------
# Example Invocation
# -----------------------------
if __name__ == "__main__":
    response = handle_return_request(
        order_id="ORD1001",
        sku="SKU123"
    )

    print(response)

