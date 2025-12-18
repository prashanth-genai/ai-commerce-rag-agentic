import pytest
from agents.order_agent import handle_order_query

def test_order_status():
    response = handle_order_query("ORD1001")

    assert response["order_id"] == "ORD1001"
    assert "status" in response
    assert "eta" in response
    assert "message" in response

