from agent_service.agent_graph import build_agent_graph

def test_intent_detection():
    graph = build_agent_graph()
    out = graph.invoke({"user_query": "please cancel my order ORD2911"})
    assert out["result"]

