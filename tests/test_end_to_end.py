"""
End-to-End Test:
User query -> AgentGraph -> Agent -> RAG -> Response
"""

from unittest.mock import patch
from agent_service.agent_graph import build_agent_graph


def test_e2e_order_tracking_flow():
    graph = build_agent_graph()

    # Mock OMS Response
    with patch("agents.order_agent.get_order_status.run") as mock_oms:
        mock_oms.return_value = {
            "order_id": "ORD5001",
            "status": "SHIPPED",
            "carrier": "BlueDart",
            "tracking_number": "BD123"
        }

        result = graph.invoke({"user_query": "Where is my order ORD5001?"})

        assert "result" in result
        assert result["result"]["status"] == "SHIPPED"


def test_e2e_cancellation_flow():
    graph = build_agent_graph()

    with patch("agents.cancel_agent.get_order_status.run") as mock_fetch:
        mock_fetch.return_value = {
            "order_id": "ORD9002",
            "status": "PROCESSING",
            "payment_status": "PAID",
            "items": [{"sku": "SKU1001", "price": 1999}]
        }

        result = graph.invoke({"user_query": "cancel my order ORD9002"})

        assert "result" in result
        assert "refund_amount" in result["result"]

