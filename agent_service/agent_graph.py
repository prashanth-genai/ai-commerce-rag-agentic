from langgraph.graph import StateGraph
from agent_service.agents.intent_agent import detect_intent
from agent_service.agents.order_agent import handle_order

def intent_node(state):
    state["intent"] = detect_intent(state["query"])
    return state

def order_node(state):
    state["result"] = handle_order(state["user_id"])
    return state

graph = StateGraph(dict)
graph.add_node("intent", intent_node)
graph.add_node("order", order_node)

graph.set_entry_point("intent")
graph.add_edge("intent", "order")

agent_executor = graph.compile()

