
from agents.cancel_agent import handle_order_cancellation

def test_cancel_order():
    resp = handle_order_cancellation("ORD9001")
    assert "eligible" in resp
    assert "refund_amount" in resp
    assert " cancel" or "Cancel" in resp["message"]
