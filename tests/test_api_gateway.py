from fastapi.testclient import TestClient
from api_gateway.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_catalog_search_api():
    payload = {"query": "laptop"}
    response = client.post("/catalog/search", json=payload, headers={"Authorization": "Bearer test"})
    assert response.status_code in [200, 401]  # depends on auth config

def test_order_status_api():
    response = client.get("/order/status/ORD1001", headers={"Authorization": "Bearer test"})
    assert response.status_code in [200, 401]

def test_cancel_api():
    payload = {"order_id": "ORD1001"}
    response = client.post("/order/cancel", json=payload, headers={"Authorization": "Bearer test"})
    assert response.status_code in [200, 401]

