"""
Cancel Agent
------------
AI agent to handle order cancellation requests using:
✔ OMS data
✔ RAG-based cancellation policy
✔ Refund rules
✔ Agentic decision workflow

Domain: eCommerce (B2C / B2B)
"""

from datetime import datetime
from typing import Dict, Any
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.schema import AIMessage

# --------------------------------
# LLM CONFIG
# --------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)

# --------------------------------
# TOOLS (OMS + POLICY + PAYMENT)
# --------------------------------

@tool
def get_order_status(order_id: str) -> Dict[str, Any]:
    """
    Simulate OMS call for order status.
    """
    return {
        "order_id": order_id,
        "status": "PROCESSING",   # PROCESSING | SHIPPED | DELIVERED
        "order_date": "2024-10-10",
        "payment_status": "PAID",
        "items": [
            {"sku": "SKU1001", "price": 2999, "quantity": 1}
        ]
    }


@tool
def get_cancellation_policy() -> Dict[str, Any]:
    """
    RAG-based policy retrieval from vector DB.
    """
    return {
        "cancellable_statuses": ["ORDER_PLACED", "PROCESSING"],
        "refund_processing_days": 5,
        "restocking_fee_percent": 0  # not applicable for cancellation
    }


@tool
def cancel_order_in_oms(order_id: str) -> str:
    """
    Simulated OMS cancel API call.
    """
    return f"CANCEL_REQ_{order_id}"


@tool
def calculate_refund_on_cancel(price: float, payment_status: str) -> float:
    """
    Refund calculation for cancellation.
    """
    if payment_status == "PAID":
        return price
    return 0.0


# --------------------------------
# PROMPT TEMPLATE
# --------------------------------
cancel_prompt = PromptTemplate(
    input_variables=[
        "order_id",
        "status",
        "refundable",
        "refund_amount",
        "policy",
        "cancel_request_id"
    ],
    template="""
You are an AI Order Cancellation Assistant.

Order ID: {order_id}
Order Status: {status}
Refund Eligible: {refundable}
Refund Amount: ₹{refund_amount}

Cancellation Policy:
{policy}

If cancellation is allowed:
- Explain the refund amount
- Explain the next steps
- Provide the cancellation confirmation ID: {cancel_request_id}

If cancellation is NOT allowed:
- Politely explain why
- Offer alternatives such as return or replacement

Tone: Professional, clear, customer-friendly.
"""
)

# --------------------------------
# MAIN AGENT ORCHESTRATOR
# --------------------------------
def handle_order_cancellation(order_id: str) -> Dict[str, Any]:

    # Step 1: Fetch OMS order status
    order = get_order_status.run(order_id)
    status = order["status"]

    # Step 2: Fetch cancellation policy (RAG)
    policy = get_cancellation_policy.run()
    allowed_statuses = policy["cancellable_statuses"]

    # Step 3: Validate eligibility
    refundable = status in allowed_statuses

    if refundable:
        # Step 4: Refund amount calculation
        item = order["items"][0]
        refund_amount = calculate_refund_on_cancel.run(
            price=item["price"],
            payment_status=order["payment_status"]
        )

        # Step 5: Trigger OMS cancel request
        cancel_id = cancel_order_in_oms.run(order_id)
    else:
        refund_amount = 0
        cancel_id = "NOT_APPLICABLE"

    # Step 6: LLM response preparation
    response = llm.invoke(
        cancel_prompt.format(
            order_id=order_id,
            status=status,
            refundable="YES" if refundable else "NO",
            refund_amount=refund_amount,
            policy=policy,
            cancel_request_id=cancel_id
        )
    )

    return {
        "order_id": order_id,
        "eligible": refundable,
        "refund_amount": refund_amount,
        "cancel_request_id": cancel_id,
        "message": response.content
    }


# --------------------------------
# EXAMPLE RUN
# --------------------------------
if __name__ == "__main__":
    print(handle_order_cancellation("ORD9001"))

