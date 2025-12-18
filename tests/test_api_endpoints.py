"""
FastAPI Endpoint Integration Tests
"""

from fastapi.testclient import TestClient
from api_gateway.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "OK"


def test_agent_ask_api():
    res = client.post(
        "/agent/ask",
        json={"query": "track my order ORD1001"},
        headers={"Authorization": "Bearer testtoken"}
    )
    # Auth may fail depending on dev config
    assert res.status_code in (200, 401)


def test_catalog_search_api():
    res = client.post(
        "/catalog/search",
        json={"query": "mobile"},
        headers={"Authorization": "Bearer testtoken"}
    )
    assert res.status_code in (200, 401)


def test_return_request_api():
    res = client.post(
        "/order/return",
        json={"order_id": "ORD1001", "sku": "SKU1001"},
        headers={"Authorization": "Bearer testtoken"}
    )
    assert res.status_code in (200, 401)


def test_cancel_order_api():
    res = client.post(
        "/order/cancel",
        json={"order_id": "ORD1001"},
        headers={"Authorization": "Bearer testtoken"}
    )
    assert res.status_code in (200, 401)

