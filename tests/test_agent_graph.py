from agent_service.agent_graph import build_agent_graph

def test_agent_graph_order_flow():
    graph = build_agent_graph()
    resp = graph.invoke({"user_query": "track order ORD1001"})
    assert "result" in resp
    assert "status" in resp["result"]
#####
"""
Tests for AgentGraph (LangGraph multi-agent orchestration)
"""

from agent_service.agent_graph import build_agent_graph

def test_agent_graph_order_status():
    graph = build_agent_graph()
    result = graph.invoke({"user_query": "track my order ORD1234"})

    assert "result" in result
    assert "status" in result["result"]
    assert "message" in result["result"]

def test_agent_graph_cancellation_route():
    graph = build_agent_graph()
    result = graph.invoke({"user_query": "cancel order ORD7812"})

    assert "result" in result
    assert "message" in result["result"]

def test_agent_graph_unknown_intent():
    graph = build_agent_graph()
    result = graph.invoke({"user_query": "blabla random nonsense"})

    assert "result" in result
    assert "message" in result["result"]

