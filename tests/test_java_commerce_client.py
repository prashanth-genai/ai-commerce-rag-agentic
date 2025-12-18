import requests
from unittest.mock import patch
from integration.java_commerce_client import fetch_order

@patch("requests.get")
def test_fetch_order(mock_get):
    mock_get.return_value.json.return_value = {"order_id": "ORD1001"}

    result = fetch_order("ORD1001")
    assert result["order_id"] == "ORD1001"

