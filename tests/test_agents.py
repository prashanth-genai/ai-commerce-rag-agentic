"""
Tests for all commerce agents:
- Catalog Agent
- Order Agent
- Return Agent
- Cancel Agent
"""

import pytest

from agents.catalog_agent import handle_catalog_query
from agents.order_agent import handle_order_query
from agents.return_agent import handle_return_request
from agents.cancel_agent import handle_order_cancellation


# -----------------------------
# Catalog Agent Tests
# -----------------------------

def test_catalog_agent_response_format():
    result = handle_catalog_query("phones")

    assert isinstance(result, dict)
    assert "products" in result
    assert "message" in result


def test_catalog_agent_empty_query():
    result = handle_catalog_query("")
    assert "products" in result


# -----------------------------
# Order Agent Tests
# -----------------------------

def test_order_agent_status():
    order_id = "ORD1001"
    res = handle_order_query(order_id)

    assert res["order_id"] == order_id
    assert "status" in res
    assert "eta" in res
    assert "message" in res


def test_order_agent_invalid_id():
    res = handle_order_query("INVALID")
    assert "message" in res


# -----------------------------
# Return Agent Tests
# -----------------------------

def test_return_agent_flow():
    res = handle_return_request("ORD1001", "SKU1001")

    assert "eligible" in res
    assert "refund_amount" in res
    assert "message" in res


def test_return_agent_invalid_sku():
    res = handle_return_request("ORD1001", "BADSKU")
    assert "message" in res


# -----------------------------
# Cancel Agent Tests
# -----------------------------

def test_cancel_agent_flow():
    res = handle_order_cancellation("ORD9001")

    assert "eligible" in res
    assert "refund_amount" in res
    assert "cancel_request_id" in res
    assert "message" in res


def test_cancel_agent_blocked_case():
    # Try cancelling a delivered order (mock response will trigger logic)
    res = handle_order_cancellation("ORD_DELIVERED")
    assert "message" in res  # Should contain explanation

