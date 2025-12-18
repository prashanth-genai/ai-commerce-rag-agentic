"""
java_commerce_client.py
-----------------------

Integration layer between Python AI (Agents, RAG, LangGraph)
and Java/Spring Boot microservices (Catalog, OMS, Pricing, Inventory, Shipping).

This is a production-grade HTTP client with:
✔ Timeout & retry logic
✔ Centralized request handler
✔ Consistent response format
✔ Exception handling
✔ Extensible for future microservices
"""

import os
import requests
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter, Retry


# ---------------------------------------------------------
# Configuration (Base URL from Env)
# ---------------------------------------------------------

BASE_URL = os.getenv("JAVA_COMMERCE_BASE_URL", "http://localhost:8080")


# ---------------------------------------------------------
# Session with Retry & Timeout Handling
# ---------------------------------------------------------

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET", "POST", "PUT"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)


# ---------------------------------------------------------
# Helper: Unified HTTP Wrapper
# ---------------------------------------------------------

def http_call(method: str, url: str, payload: Optional[Dict] = None) -> Dict[str, Any]:
    """
    A unified HTTP handler used by all commerce API calls.
    """
    try:
        if method == "GET":
            resp = session.get(url, timeout=4)
        elif method == "POST":
            resp = session.post(url, json=payload, timeout=5)
        elif method == "PUT":
            resp = session.put(url, json=payload, timeout=5)
        else:
            raise ValueError("Unsupported HTTP method")

        resp.raise_for_status()  # throws error if >= 400
        return resp.json()

    except requests.exceptions.Timeout:
        return {"error": "Timeout", "url": url}

    except requests.exceptions.ConnectionError:
        return {"error": "ConnectionError", "url": url}

    except Exception as ex:
        return {"error": str(ex), "url": url}


# ---------------------------------------------------------
# CATALOG SERVICE
# ---------------------------------------------------------

def fetch_product_by_sku(sku: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/catalog/product/{sku}"
    return http_call("GET", url)


def search_catalog(query: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/catalog/search?q={query}"
    return http_call("GET", url)


# ---------------------------------------------------------
# ORDER MANAGEMENT SERVICE (OMS)
# ---------------------------------------------------------

def fetch_order(order_id: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/oms/order/{order_id}"
    return http_call("GET", url)


def cancel_order(order_id: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/oms/order/{order_id}/cancel"
    return http_call("POST", url)


def fetch_order_items(order_id: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/oms/order/{order_id}/items"
    return http_call("GET", url)


def fetch_order_exceptions(order_id: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/oms/order/{order_id}/exceptions"
    return http_call("GET", url)


# ---------------------------------------------------------
# PRICING SERVICE (B2B + CONTRACTS)
# ---------------------------------------------------------

def fetch_price(customer_id: str, sku: str) -> Dict[str, Any]:
    """
    B2B contract pricing lookup.
    """
    url = f"{BASE_URL}/pricing/contract/{customer_id}/{sku}"
    return http_call("GET", url)


def fetch_bulk_pricing(sku: str, quantity: int) -> Dict[str, Any]:
    """
    Tiered/bulk discount pricing.
    """
    url = f"{BASE_URL}/pricing/bulk?sku={sku}&qty={quantity}"
    return http_call("GET", url)


# ---------------------------------------------------------
# INVENTORY SERVICE
# ---------------------------------------------------------

def fetch_inventory(sku: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/inventory/{sku}"
    return http_call("GET", url)


# ---------------------------------------------------------
# SHIPPING SERVICE
# ---------------------------------------------------------

def fetch_shipping_eta(tracking_no: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/shipping/eta/{tracking_no}"
    return http_call("GET", url)


# ---------------------------------------------------------
# QUICK SELF-TEST
# ---------------------------------------------------------

if __name__ == "__main__":
    print(fetch_order("ORD1001"))
    print(fetch_price("CUST32", "SKU8823"))
    print(fetch_inventory("SKU1001"))

