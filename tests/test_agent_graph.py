from agent_service.agent_graph import build_agent_graph

def test_agent_graph_order_flow():
    graph = build_agent_graph()
    resp = graph.invoke({"user_query": "track order ORD1001"})
    assert "result" in resp
    assert "status" in resp["result"]

