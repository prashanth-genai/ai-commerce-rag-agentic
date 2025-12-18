import requests

def handle_order(user_id):
    response = requests.get(
        f"http://java-commerce-mock/order-service/orders/{user_id}"
    )
    return response.json()

----
"""
Order Agent
-----------
AI agent responsible for order tracking, status explanation,
delivery ETA reasoning, and exception handling using
RAG + enterprise microservices.

Domain: eCommerce (B2C / B2B)
"""

from typing import Dict, Any
from datetime import datetime, timedelta
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
# Tools (OMS + Logistics)
# -----------------------------

@tool
def get_order_status(order_id: str) -> Dict[str, Any]:
    """
    Fetch order status from Order Service (Java OMS).
    """
    return {
        "order_id": order_id,
        "status": "SHIPPED",
        "order_date": "2024-10-10",
        "shipment_date": "2024-10-11",
        "carrier": "BlueDart",
        "tracking_number": "BD123456"
    }


@tool
def get_delivery_eta(carrier: str, tracking_number: str) -> str:
    """
    Get ETA from logistics provider.
    """
    return "Expected delivery by 2024-10-15"


@tool
def get_order_exceptions(order_id: str) -> Dict[str, Any]:
    """
    Check for any delivery or payment exceptions.
    """
    return {
        "exception": None,
        "notes": "No issues detected"
    }


# -----------------------------
# Prompt Template
# -----------------------------
order_prompt = PromptTemplate(
    input_variables=[
        "order_id",
        "status",
        "carrier",
        "tracking_number",
        "eta",
        "exception"
    ],
    template="""
You are an AI Order Support Agent for an enterprise eCommerce platform.

Order ID: {order_id}
Current Status: {status}
Carrier: {carrier}
Tracking Number: {tracking_number}
Estimated Delivery: {eta}

Exceptions:
{exception}

Explain clearly:
1. Current order status
2. Delivery timeline
3. Any action required by customer
Use a calm, reassuring, and professional tone.
"""
)

# -----------------------------
# Agent Orchestration Logic
# -----------------------------
def handle_order_query(order_id: str) -> Dict[str, Any]:
    """
    Main orchestration function for order tracking workflow.
    """

    # Step 1: Fetch order status
    order = get_order_status.run(order_id)

    # Step 2: Fetch delivery ETA
    eta = get_delivery_eta.run(
        order["carrier"],
        order["tracking_number"]
    )

    # Step 3: Check exceptions
    exception_info = get_order_exceptions.run(order_id)

    # Step 4: Generate AI response
    prompt = order_prompt.format(
        order_id=order_id,
        status=order["status"],
        carrier=order["carrier"],
        tracking_number=order["tracking_number"],
        eta=eta,
        exception=exception_info["notes"]
    )

    ai_response: AIMessage = llm.invoke(prompt)

    return {
        "order_id": order_id,
        "status": order["status"],
        "eta": eta,
        "message": ai_response.content
    }


# -----------------------------
# Example Invocation
# -----------------------------
if __name__ == "__main__":
    response = handle_order_query("ORD2001")
    print(response)
